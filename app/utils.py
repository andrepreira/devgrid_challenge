import time
import asyncio

import aiohttp

from app.configs import AppSettings
from app.schemas import WeatherDataCreate, Weather
from app.constants import API_DELAY_IN_SECONDS
settings = AppSettings()
api_key = settings.weather_api_key


async def fetch_weather(session: aiohttp.ClientSession, city_id: str) -> dict:
    time.sleep(API_DELAY_IN_SECONDS)
    url = f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}&units=metric"
    async with session.get(url) as response:
        return await response.json()


async def fetch_all_weather_data(city_ids: list) -> list:
    async with aiohttp.ClientSession() as session:
        tasks = []
        for city_id in city_ids:
            tasks.append(fetch_weather(session, city_id))
        return await asyncio.gather(*tasks)


def parse_weather_data(data: dict) -> WeatherDataCreate:
    weather =  Weather(
        city_id=data.get("id"),
        temperature=data.get("main").get("temp"),
        humidity=data.get("main").get("humidity")
    )
    
    return WeatherDataCreate(
        **weather.model_dump(),
        data=weather.model_dump_json(),
    )
