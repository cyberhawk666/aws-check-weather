import json
import requests
import boto3
from datetime import datetime

API_KEY = "c31db2630f7e847a84234b0f2d7bbac5"
CITIES = ["New York", "London", "Mumbai", "Tokyo"]

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('WeatherData')

def lambda_handler(event, context):
    for city in CITIES:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()
        if response.get("main"):
            table.put_item(Item={
                'City': city,
                'Timestamp': datetime.utcnow().isoformat(),
                'Temperature': response["main"]["temp"],
                'Humidity': response["main"]["humidity"],
                'WindSpeed': response["wind"]["speed"],
                'Condition': response["weather"][0]["main"]
            })
    return {
        'statusCode': 200,
        'body': json.dumps('Weather data updated successfully!')
    }
