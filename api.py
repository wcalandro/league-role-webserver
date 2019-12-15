from __future__ import print_function
from roleml import roleml
from flask import Flask, escape, request, jsonify
from riotwatcher import RiotWatcher, ApiError

# Get RIOT_API_KEY from environment
import os
riot_key = os.getenv("RIOT_API_KEY")
if riot_key is None:
    print("No Riot API key provided!")
    exit(1)

watcher = RiotWatcher(riot_key)

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/getRolesForMatch", methods=['GET'])
def getRolesForMatch():
    match_id = request.args.get("match_id")
    if match_id is None:
        return jsonify({
            "success": False,
            "error": "match_id not set"
        })
    else:
        match = watcher.match.by_id("NA1", int(match_id))
        timeline = watcher.match.timeline_by_match("NA1", int(match_id))
        prediction = roleml.predict(match, timeline)
        summoner_names = [summoner["player"]["summonerName"]
                          for summoner in match["participantIdentities"]]
        role_to_name = {
            "blue": {
                "top": "",
                "jungle": "",
                "mid": "",
                "bot": "",
                "supp": ""
            },
            "red": {
                "top": "",
                "jungle": "",
                "mid": "",
                "bot": "",
                "supp": ""
            }
        }
        name_to_role = {}
        for id in prediction:
            if int(id) < 6:
                role_to_name["blue"][prediction[id]
                                     ] = summoner_names[int(id)-1]
                name_to_role[summoner_names[int(
                    id)-1]] = {"team": "blue", "position": prediction[id]}
            else:
                role_to_name["red"][prediction[id]] = summoner_names[int(id)-1]
                name_to_role[summoner_names[int(
                    id)-1]] = {"team": "red", "position": prediction[id]}
        return jsonify({
            "success": True,
            "roles": role_to_name,
            "names": name_to_role,
            "match": match
        })


app.run()
