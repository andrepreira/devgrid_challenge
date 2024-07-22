import logging

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas, utils
from app.constants import CITY_ID_LIST
from app.database import get_db

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/weather", response_model=schemas.RequestLogResponse, status_code=202)
async def collect_weather_data(
    username: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    username_verify = crud.get_request_log_by_username(db=db, username=username)
    if username_verify:
        raise HTTPException(status_code=400, detail="Username already exists")

    city_ids = CITY_ID_LIST
    request_log = schemas.RequestLogCreate(
        username=username, total_cities=len(city_ids)
    )
    db_request_log = crud.create_request_log(db=db, request_log=request_log)

    background_tasks.add_task(utils.process_data, db, city_ids, db_request_log)
    return {"message": "Processing started", "username": username}


@router.get("/progress/{username}", response_model=schemas.ProgressResponse)
def get_progress(username: str, db: Session = Depends(get_db)):
    db_request_log = crud.get_request_log_by_username(db=db, username=username)
    if not db_request_log:
        raise HTTPException(status_code=404, detail="Request not found")
    progress = (db_request_log.cities_collected / db_request_log.total_cities) * 100
    return {"username": username, "progress": progress}
