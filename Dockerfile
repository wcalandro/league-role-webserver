FROM python:buster

WORKDIR /app
ADD . .
RUN pip install -r requirements.txt
RUN pip install waitress

EXPOSE 5000

CMD ["python", "api.py"]