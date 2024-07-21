from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from app.crud import (
    create_request_log,
    create_weather_data,
    get_request_log_by_username,
    get_weather_data_by_city_id,
    update_request_log,
)
from app.models import RequestLog, WeatherData
from app.schemas import RequestLogCreate, Weather, WeatherDataCreate


@pytest.fixture
def mock_db_session():
    db = MagicMock(spec=Session)
    yield db


def test_create_weather_data(mock_db_session):
    data = Weather(city_id=1, temperature=25.5, humidity=60)

    weather_data_create = WeatherDataCreate(
        data=data.model_dump_json(), **data.model_dump()
    )
    request_log = RequestLog(username="test_user")
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()
    mock_db_session.refresh = MagicMock()

    result = create_weather_data(mock_db_session, weather_data_create, request_log)

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    assert isinstance(result, WeatherData)


def test_create_request_log(mock_db_session):
    request_log_create = RequestLogCreate(
        username="test_user", cities_collected=5, total_cities=10
    )
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()
    mock_db_session.refresh = MagicMock()

    result = create_request_log(mock_db_session, request_log_create)

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    assert isinstance(result, RequestLog)


def test_get_request_log_by_username(mock_db_session):
    username = "test_user"
    mock_db_session.query.return_value.filter.return_value.first.return_value = (
        RequestLog(username=username)
    )

    result = get_request_log_by_username(mock_db_session, username)

    mock_db_session.query.assert_called_once_with(RequestLog)
    mock_db_session.query.return_value.filter.assert_called_once()
    assert result.username == username


def test_update_request_log(mock_db_session):
    request_log = RequestLog(username="test_user")
    cities_collected = 10
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()
    mock_db_session.refresh = MagicMock()

    result = update_request_log(mock_db_session, request_log, cities_collected)

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    assert result.cities_collected == cities_collected


def test_get_weather_data_by_city_id(mock_db_session):
    city_id = 1
    mock_db_session.query.return_value.filter.return_value.first.return_value = (
        WeatherData(city_id=city_id)
    )

    result = get_weather_data_by_city_id(mock_db_session, city_id)

    mock_db_session.query.assert_called_once_with(WeatherData)
    mock_db_session.query.return_value.filter.assert_called_once()
    assert result.city_id == city_id
