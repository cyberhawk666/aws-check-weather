import streamlit as st
import requests
import pandas as pd
import boto3
import json

# -------- CONFIG --------
API_KEY = "c31db2630f7e847a84234b0f2d7bbac5"
CITIES = ["New York", "London", "Mumbai", "Tokyo"]
data = [
    {"City": "London", "Temperature": 22, "Humidity": 55},
    {"City": "Paris", "Temperature": 24, "Humidity": 60},
    {"City": "New York", "Temperature": 28, "Humidity": 65}
]

df = pd.DataFrame(data)

# Optional: DynamoDB setup
# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('WeatherData')

st.title("AWS Cloud Weather Dashboard 🌤️")

# Sidebar: select cities
selected_cities = st.multiselect("Select cities", CITIES, default=CITIES[:2])

weather_data = []

for city in selected_cities:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        weather = {
            "City": city,
            "Temperature": response["main"]["temp"],
            "Humidity": response["main"]["humidity"],
            "Wind Speed": response["wind"]["speed"],
            "Condition": response["weather"][0]["main"]
        }
        weather_data.append(weather)

# Display DataFrame
df = pd.DataFrame(weather_data)
st.table(df)

# Optional: Charts
st.subheader("Temperature Comparison")
st.bar_chart(df.set_index("City")["Temperature"])

# Optional: Alerts~
THRESHOLD_TEMP = 35
for w in weather_data:
    if w["Temperature"] > THRESHOLD_TEMP:
        st.warning(f"⚠️ {w['City']} temperature is above {THRESHOLD_TEMP}°C!")

# Optional: Push alerts via AWS SNS
# sns_client = boto3.client('sns')
# for w in weather_data:
#     if w["Temperature"] > THRESHOLD_TEMP:
#         sns_client.publish(
#             TopicArn="YOUR_SNS_TOPIC_ARN",
#             Message=f"{w['City']} temperature is {w['Temperature']}°C!",
#             Subject="Weather Alert"
#         )
