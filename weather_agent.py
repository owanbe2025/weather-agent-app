import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key loaded? {openai_api_key is not None}")

# Load your OpenWeatherMap API key from .env
weather_api_key = os.getenv("OPENWEATHER_API_KEY")
print(f"Weather API Key loaded? {weather_api_key is not None}")

def get_weather(location: str):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": weather_api_key,
        "units": "metric"
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        description = data["weather"][0]["description"]

        return (
            f"🌦️ The weather in {location} is currently **{description}**.\n"
            f"🌡️ Temperature: {temp}°C (feels like {feels_like}°C).\n"
            f"💧 Humidity: {humidity}%.\n"
            f"💨 Wind Speed: {wind_speed} m/s."
        )
    else:
        return "Sorry, I couldn’t fetch the weather information."



if __name__ == "__main__":
    location = input("Enter a city to check the weather: ")
    print(get_weather(location))

