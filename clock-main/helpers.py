from config import (
    engine, covid_api,
    weather_api_key,
    news_api_key
)
import requests, time
#text-to-speech
def makeAnnouncement(message):
    try:
        print(f"Making an announcement for {message}")
        engine.say(message)
        engine.runAndWait()
    except Exception as e:
        print(e)
        return None

def getCovidUpdate():
    try:
        print("Getting covid 19 updates from covid api")
        return covid_api.get_json()["data"][0]
    except Exception as e:
        print(e)
        return None
#the weathers api
def getWeatherUpdate():
    try:
        print("Getting weather updates from weather api")
        r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q=Exeter&appid={weather_api_key}&units=metric')
        if r.status_code == 200:
            return r.json()
        else:
            print(f"Weather API error: {r.message}")
            return None
    except Exception as e:
        print(e)
        return None
#the news api
def getNewsUpdate():
    try:
        print("Getting news updates from news api")
        r = requests.get(f'https://newsapi.org/v2/top-headlines?country=gb&apiKey={news_api_key}')
        if r.status_code == 200:
            return r.json()["articles"][0]
        else:
            print(f"News API error: {r.message}")
            return None
    except Exception as e:
        print(e)
        return None

def getRemainingSeconds(time_string):
    try:
        print("Calculating remaining seconds in making announcement")
        # Taking the string representation of time and converting it
        # to respective time tuple with strptime function
        # Then passing the time tuple to the mktime function to get
        # the number of seconds elapsed since the epoch (01/01/1970, midnight)
        future_time = time.mktime(time.strptime(time_string, "%Y-%m-%dT%H:%M"))
        current_time = time.time()
        if future_time > current_time:
            return future_time - current_time
        print("Incorrect time provided, could not schedule announcement")
        return None
    except Exception as e:
        print(e)
        return None