import requests
from pydantic import BaseModel
from configs import AppSettings

app_settings = AppSettings(_env_file=".env")

class Weather(BaseModel):
    city_id: int
    temp: float
    humidity: int

class WeatherData(BaseModel):
    id: int
    data: Weather
    
city_id=3439525
api_key = app_settings.weather_api_key
url = f"https://api.openweathermap.org/data/2.5/weather"

params = {
    'id': city_id,
    'appid': api_key,
    'units': 'metric'
}

response = requests.request("GET", url, params=params)
response.raise_for_status()
response_json = response.json()

weather = Weather(
    city_id=city_id,
    temp=response_json['main']['temp'],
    humidity=response_json['main']['humidity'],
).model_dump()

weather = WeatherData(id=1, data=weather).model_dump()
print(weather)