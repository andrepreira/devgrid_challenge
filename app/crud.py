from sqlalchemy.orm import Session

from app.models import RequestLog, WeatherData
from app.schemas import RequestLogCreate, WeatherDataCreate


def create_weather_data(db: Session, weather_data: WeatherDataCreate, request_log: RequestLog):
    db_weather_data = WeatherData(**weather_data.model_dump(), username=request_log.username)
    db.add(db_weather_data)
    db.commit()
    db.refresh(db_weather_data)
    return db_weather_data


def create_request_log(db: Session, request_log: RequestLogCreate):
    db_request_log = RequestLog(**request_log.model_dump())
    db.add(db_request_log)
    db.commit()
    db.refresh(db_request_log)
    return db_request_log


def get_request_log_by_username(db: Session, username: str):
    return (
        db.query(RequestLog)
        .filter(RequestLog.username == username)
        .first()
    )


def update_request_log(db: Session, request_log: RequestLog, cities_collected: int):
    request_log.cities_collected = cities_collected
    db.add(request_log)
    db.commit()
    db.refresh(request_log)
    return request_log


def get_weather_data_by_city_id(db: Session, city_id: int):
    return db.query(WeatherData).filter(WeatherData.city_id == city_id).first()
