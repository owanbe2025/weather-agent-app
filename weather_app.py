import os
import requests
from dotenv import load_dotenv
import streamlit as st
from streamlit_folium import st_folium
import folium

# Load API keys
load_dotenv()
weather_api_key = os.getenv("OPENWEATHER_API_KEY")
base_url = "https://api.openweathermap.org/data/2.5/weather"
forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

# Weather function
def get_weather(location: str):
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
        icon = data["weather"][0]["icon"]

        icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"

        report = (
            f"🌦️ **Weather in {location}**\n\n"
            f"![Weather Icon]({icon_url})\n\n"
            f"🌡️ **Temperature**: {temp}°C (feels like {feels_like}°C)\n\n"
            f"💧 **Humidity**: {humidity}%\n\n"
            f"💨 **Wind Speed**: {wind_speed} m/s\n\n"
            f"📝 **Description**: {description.capitalize()}"
        )
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]
        return report, lat, lon
    else:
        return "❌ Sorry, I couldn’t fetch the weather information.", None, None

# Forecast function
def get_forecast(location: str):
    params = {
        "q": location,
        "appid": weather_api_key,
        "units": "metric",
        "cnt": 40
    }

    response = requests.get(forecast_url, params=params)
    if response.status_code == 200:
        data = response.json()
        forecast_list = data["list"]

        daily_forecast = {}
        for entry in forecast_list:
            date = entry["dt_txt"].split(" ")[0]
            temp = entry["main"]["temp"]
            description = entry["weather"][0]["description"]
            if date not in daily_forecast:
                daily_forecast[date] = {
                    "temps": [temp],
                    "descriptions": [description]
                }
            else:
                daily_forecast[date]["temps"].append(temp)
                daily_forecast[date]["descriptions"].append(description)

        forecast_summary = ""
        for date, info in daily_forecast.items():
            avg_temp = sum(info["temps"]) / len(info["temps"])
            main_desc = max(set(info["descriptions"]), key=info["descriptions"].count)
            forecast_summary += (
                f"📅 **{date}**\n"
                f"🌡️ Avg Temp: {avg_temp:.1f}°C\n"
                f"📝 Condition: {main_desc.capitalize()}\n\n"
            )

        return forecast_summary
    else:
        return "❌ Sorry, I couldn’t fetch the forecast information."

# Streamlit app
st.set_page_config(page_title="🌍 Weather App", page_icon="🌦️")
st.markdown(
    """
    <style>
    .reportview-container {
        background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%);
        color: #000000;
    }
    .stButton>button {
        color: white;
        background-color: #007BFF;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌍 Weather Checker")
st.markdown("Enter a city to see the current weather and forecast! 🌦️")

city = st.text_input("City Name", "Belfast")

# Use session state to remember city and weather data
if "city" not in st.session_state:
    st.session_state.city = None
if "lat" not in st.session_state:
    st.session_state.lat = None
if "lon" not in st.session_state:
    st.session_state.lon = None

# Check Weather button logic
if st.button("Check Weather 🌦️"):
    weather_report, lat, lon = get_weather(city)
    st.session_state.weather_report = weather_report
    st.session_state.city = city
    st.session_state.lat = lat
    st.session_state.lon = lon

# Always display the weather report if it exists
if "weather_report" in st.session_state:
    st.markdown(st.session_state.weather_report, unsafe_allow_html=True)

# Always show the map and forecast buttons if lat/lon exist
if st.session_state.get("lat") and st.session_state.get("lon"):
    if st.button("Show Map 🗺️"):
        m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=10)
        folium.Marker([st.session_state.lat, st.session_state.lon], popup=st.session_state.city).add_to(m)
        st_folium(m, width=700)

    if st.button("Show 5-Day Forecast 📅"):
        forecast = get_forecast(st.session_state.city)
        st.markdown(forecast)
