from flask import render_template, request
from helpers import (
    getRemainingSeconds,
    makeAnnouncement,
    getWeatherUpdate,
    getCovidUpdate,
    getNewsUpdate
)
from threading import Timer
from config import schedule, covid_api

alarms = []
notifications = {}

def index():
    global alarms
    alarm = {}
    alarm_datetime = request.args.get("alarm")
    title = request.args.get("title")
    alarm_title = request.args.get("alarm_item")

    if alarm_title is not None:
        print(f"Deleting the {alarm_title} alarm")
        filtered_alarms = filter(lambda alarm: alarm["title"] != alarm_title, alarms)
        alarms = list(filtered_alarms)
    notification_title = request.args.get("notification_item")

    if notification_title is not None:
        if notification_title == "Covid 19 Update":
            print("Deleting the covid update notification")
            del notifications["covid"]
        elif notification_title == "News Update":
            print("Deleting the news update notification")
            del notifications["news"]
        else:
            print("Deleting the weather update notification")
            del notifications["weather"]

    if alarm_datetime is not None and title is not None:
        alarm["title"] = title
        alarm["content"] = title
        alarms.append(alarm)
        delay = getRemainingSeconds(alarm_datetime)

        if delay is not None:
            # Timer(delay, makeAnnouncement, (title,)).start()
            schedule.enter(delay, 1, makeAnnouncement, (title,))
            schedule.run(blocking=False)
        covid_data = getCovidUpdate()

        if covid_data is not None:
            print("Creating the covid update notification")
            notifications["covid"] = {
                "title": "England Covid 19 Update",
                "content": f'In {covid_data["areaName"]}, there is {covid_data["newCasesByPublishDate"]} new cases and {covid_data["cumCasesByPublishDate"]} total cases!'
            }
#news update
    if request.args.get("news"):
        news_data = getNewsUpdate()
        if news_data is not None:
            print("Creating the news update notification")
            notifications["news"] = {
                "title": "News Update",
                "content": news_data["description"]
            }
#weather update
    if request.args.get("weather"):
        weather_data = getWeatherUpdate()
        if weather_data is not None:
            print("Creating the weather update notification")
            notifications["weather"] = {
                "title": "Exeter Weather Update",
                "content": f'Today\'s temperature is {weather_data["main"]["temp"]}C and \
                    it feels like {weather_data["main"]["feels_like"]}C. \
                    Pressure: {weather_data["main"]["pressure"]}Pa, \
                    Humidity: {weather_data["main"]["humidity"]}%'
            }
    return render_template('index.html', alarms=alarms, title="alarm", image="alarm-meme.jpg", notifications=notifications.values())