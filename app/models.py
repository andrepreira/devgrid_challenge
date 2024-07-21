from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, Float 
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, index=True)
    temperature = Column(Float)
    humidity = Column(Integer)
    data = Column(JSON)
    username = Column(String, ForeignKey("request_log.username"))
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    
    request_log = relationship("RequestLog", back_populates="weather_data")


class RequestLog(Base):
    __tablename__ = "request_log"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    total_cities = Column(Integer)
    cities_collected = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    
    weather_data = relationship("WeatherData", back_populates="request_log")
