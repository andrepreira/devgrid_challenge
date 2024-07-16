from pydantic import BaseModel
from datetime import datetime

class Weather(BaseModel):
    city_id: int
    temp: float
    humidity: int

class WeatherDataBase(BaseModel):
    city_id: int
    temp: float
    humidity: int
    data: Weather

class WeatherDataCreate(WeatherDataBase):
    pass

class WeatherData(WeatherDataBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class RequestLogBase(BaseModel):
    user_defined_id: str

class RequestLogCreate(RequestLogBase):
    total_cities: int

class RequestLog(RequestLogBase):
    id: int
    cities_collected: int
    timestamp: datetime

    class Config:
        from_attributes = True

class ProgressResponse(BaseModel):
    user_defined_id: str
    progress: float