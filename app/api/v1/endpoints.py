import logging

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app import crud, schemas, utils
from app.database import SessionLocal
from app.constants import CITY_ID_LIST
from app.models import RequestLog

router = APIRouter()

logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def process_data(db: Session, city_ids: list, request_log: RequestLog):
    cities_collected = 0
    weather_data = await utils.fetch_all_weather_data(city_ids)
    for data in weather_data:
        weather = utils.parse_weather_data(data)
        crud.create_weather_data(db=db, weather_data=weather)
        cities_collected += 1
        crud.update_request_log(
            db=db, request_log=request_log, cities_collected=cities_collected
        )

    return request_log
    

@router.post("/weather", response_model=schemas.RequestLogResponse, status_code=202)
async def collect_weather_data(username: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    username_verify = crud.get_request_log_by_username(db=db, username=username)
    if username_verify:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    city_ids = CITY_ID_LIST
    request_log = schemas.RequestLogCreate(
        username=username, total_cities=len(city_ids)
    )
    db_request_log = crud.create_request_log(db=db, request_log=request_log)

    background_tasks.add_task(process_data, db, city_ids, db_request_log)
    return {"message": "Processing started", "username": username}


@router.get("/progress/{username}", response_model=schemas.ProgressResponse)
def get_progress(username: str, db: Session = Depends(get_db)):
    db_request_log = crud.get_request_log_by_username(
        db=db, username=username
    )
    if not db_request_log:
        raise HTTPException(status_code=404, detail="Request not found")
    progress = (db_request_log.cities_collected / db_request_log.total_cities) * 100
    return {"username": username, "progress": progress}
