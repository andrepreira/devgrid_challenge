from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, Float, Integer, String

from app.database import Base


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, index=True)
    temperature = Column(Float)
    humidity = Column(Integer)
    data = Column(JSON)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))


class RequestLog(Base):
    __tablename__ = "request_log"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    total_cities = Column(Integer)
    cities_collected = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
