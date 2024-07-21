import asyncio

import aiohttp
from sqlalchemy.orm import Session

from app import crud
from app.configs import AppSettings
from app.constants import API_DELAY_IN_SECONDS
from app.models import RequestLog
from app.schemas import Weather, WeatherDataCreate

settings = AppSettings()
api_key = settings.weather_api_key


async def process_data(db: Session, city_ids: list, request_log: RequestLog):
    cities_collected = 0
    weather_data = await fetch_all_weather_data(city_ids)
    for data in weather_data:
        weather = parse_weather_data(data)
        crud.create_weather_data(db=db, weather_data=weather, request_log=request_log)
        cities_collected += 1
        crud.update_request_log(
            db=db, request_log=request_log, cities_collected=cities_collected
        )

    return request_log


async def fetch_weather(session: aiohttp.ClientSession, city_id: str) -> dict:
    url = f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}&units=metric"

    async with session.get(url) as response:
        return await response.json()


async def fetch_all_weather_data(city_ids: list) -> list:
    async with aiohttp.ClientSession() as session:
        tasks = []
        for city_id in city_ids:
            await asyncio.sleep(API_DELAY_IN_SECONDS)
            tasks.append(fetch_weather(session, city_id))
        return await asyncio.gather(*tasks)


def parse_weather_data(data: dict) -> WeatherDataCreate:
    weather = Weather(
        city_id=data.get("id"),
        temperature=data.get("main").get("temp"),
        humidity=data.get("main").get("humidity"),
    )

    return WeatherDataCreate(
        **weather.model_dump(),
        data=weather.model_dump_json(),
    )
