from datetime import datetime

from pydantic import BaseModel, Json

class Weather(BaseModel):
    city_id: int
    temperature: float
    humidity: int

class WeatherDataCreate(Weather):
    data: Json[Weather]

class WeatherData(Weather):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class RequestLogBase(BaseModel):
    username: str


class RequestLogCreate(RequestLogBase):
    total_cities: int


class RequestLog(RequestLogBase):
    id: int
    cities_collected: int
    timestamp: datetime

    class Config:
        from_attributes = True


class ProgressResponse(BaseModel):
    username: str
    progress: float
    
    class Config:
        from_attributes = True

class RequestLogResponse(BaseModel):
    message: str
    username: str
    
    class Config:
        from_attributes = True
