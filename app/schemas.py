from datetime import datetime

from pydantic import BaseModel, ConfigDict, Json

class Weather(BaseModel):
    city_id: int
    temperature: float
    humidity: int

class WeatherDataCreate(Weather):
    data: Json[Weather]

class WeatherData(Weather):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    timestamp: datetime

class RequestLogBase(BaseModel):
    username: str


class RequestLogCreate(RequestLogBase):
    total_cities: int


class RequestLog(RequestLogBase):
    model_config = ConfigDict(from_attributes=True)
 
    id: int
    cities_collected: int
    timestamp: datetime


class ProgressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    progress: float
    
class RequestLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    message: str
    username: str
    