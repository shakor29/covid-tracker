from flask import Flask
import pyttsx3, time, sched
from uk_covid19 import Cov19API
import json
#text-to-speech
app = Flask(__name__)
app.config["SECRET_KEY"] = "any-secret-key"
engine = pyttsx3.init("espeak", debug=True)
engine.setProperty('rate', 155)
schedule = sched.scheduler(time.time, time.sleep)
#COVID cases info (location)
england_only = [
    'areaType=nation',
    'areaName=England'
]
#the type of data gathered from covid api
cases_and_deaths = {
    "date": "date",
    "areaName": "areaName",
    "areaCode": "areaCode",
    "newCasesByPublishDate": "newCasesByPublishDate",
    "cumCasesByPublishDate": "cumCasesByPublishDate",
    "newDeathsByDeathDate": "newDeathsByDeathDate",
    "cumDeathsByDeathDate": "cumDeathsByDeathDate"
}

covid_api = Cov19API(filters=england_only, structure=cases_and_deaths)
news_api_key = ""
weather_api_key = ""

with open('config.json') as json_file:
    data = json.load(json_file)
    news_api_key = data["newsApiKey"]
    weather_api_key = data["weatherApiKey"]