import requests
import os
from twilio.rest import Client
from dotenv import load_dotenv

api_key = os.getenv('API_KEY')

LAT = 19.002850
LNG = 73.014570

account_sid = os.getenv("auth_token")
auth_token = os.getenv("account_sid")
phone_num = os.getenv("PHONE_NUM")
twillio_num = os.getenv("TWILLIO_NUM")

parameters ={
    "lat": LAT,
    "lon" : LNG,
    "appid" : api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/onecall", params=parameters)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12] #slicing python lists

will_rain =False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="Bring an umbrella!",
        from_=phone_num,
        to=twillio_num
    )
    print(message.status)

hourly_weather = []
for i in range (0,13):
    code = weather_data["hourly"][i]["weather"][0]["id"]
    hourly_weather.append(code)
print(hourly_weather)

for status in hourly_weather:
    if status < 700:
        print("bring an umbrella!")
        break




