# app/utils.py
import aiohttp
import asyncio
from app.schemas import WeatherDataCreate
from app.configs import AppSettings

settings = AppSettings()
api_key = settings.weather_api_key

async def fetch_weather(session, city_id):
    url = f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}&units=metric"
    async with session.get(url) as response:
        return await response.json()

async def fetch_all_weather_data(city_ids):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for city_id in city_ids:
            tasks.append(fetch_weather(session, city_id))
        return await asyncio.gather(*tasks)

def parse_weather_data(data):
    return WeatherDataCreate(
        city_id=data['id'],
        temperature=data['main']['temp'],
        humidity=data['main']['humidity'],
        data=data
    )
