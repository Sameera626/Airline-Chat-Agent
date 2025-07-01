import requests
from dotenv import load_dotenv
import os

load_dotenv()

def get_weather(city: str) -> str:
    api_key = os.getenv("OPENWETHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"Weather in {city}: {data['weather'][0]['description']}, Temp : {data['main']['temp']}°C"
    return "Failed to fetch weather data." 