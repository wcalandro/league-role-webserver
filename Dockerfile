FROM python:buster

WORKDIR /app
ADD . .
RUN pip install -r requirements.txt
RUN pip install waitress

EXPOSE 5000

CMD ["waitress-serve",  "--port", "5000", "--call", "api:create_app"]