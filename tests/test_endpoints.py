import unittest
from http import HTTPStatus

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import models
from app.main import app

client = TestClient(app)


@unittest.mock.patch("app.utils.fetch_all_weather_data")
def test_collect_weather_data(db_session: Session):
    response = client.post("/api/v1/weather", params={"username": "test_user"})
    assert response.status_code == HTTPStatus.ACCEPTED
    assert response.json() == {"message": "Processing started", "username": "test_user"}


def test_get_progress(db_session: Session):
    request_log = models.RequestLog(
        username="test_user2",
        cities_collected=5,
        total_cities=10,
    )
    db_session.add(request_log)
    db_session.commit()

    response = client.get("/api/v1/progress/test_user2")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"username": "test_user2", "progress": 50.0}
