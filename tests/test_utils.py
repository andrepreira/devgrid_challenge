from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiohttp import ClientSession
from aioresponses import aioresponses

from app.configs import AppSettings
from app.models import RequestLog
from app.schemas import WeatherDataCreate
from app.utils import (
    fetch_all_weather_data,
    fetch_weather,
    parse_weather_data,
    process_data,
)


@pytest.fixture
def api_key():
    return AppSettings().weather_api_key


@pytest.mark.asyncio
async def test_fetch_weather(api_key):
    city_id = "123456"
    mock_response = {
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 25},
        "name": "Test City",
    }

    url = f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}&units=metric"

    with aioresponses() as m:
        m.get(url, payload=mock_response)
        async with ClientSession() as session:
            result = await fetch_weather(session, city_id)

            assert result == mock_response


@pytest.mark.asyncio
async def test_fetch_all_weather_data(api_key):
    mock_response = {"id": "12345", "main": {"temp": 25.0, "humidity": 60}}

    with aioresponses() as mock:
        urls = [
            f"http://api.openweathermap.org/data/2.5/weather?id=12345&appid={api_key}&units=metric",
            f"http://api.openweathermap.org/data/2.5/weather?id=67890&appid={api_key}&units=metric",
        ]
        for url in urls:
            mock.get(url, payload=mock_response)

        city_ids = ["12345", "67890"]
        results = await fetch_all_weather_data(city_ids)
        assert len(results) == len(city_ids)
        assert all(result["id"] == "12345" for result in results)


def test_parse_weather_data():
    mock_data = {"id": "12345", "main": {"temp": 25.0, "humidity": 60}}

    result = parse_weather_data(mock_data)

    assert isinstance(result, WeatherDataCreate)
    assert result.city_id == 12345
    assert result.temperature == 25.0
    assert result.humidity == 60


@pytest.mark.asyncio
async def test_process_data():
    mock_fetch_all_weather_data = AsyncMock()
    mock_parse_weather_data = MagicMock()
    mock_create_weather_data = MagicMock()
    mock_update_request_log = MagicMock()

    city_ids = [1, 2, 3]
    request_log = RequestLog()
    weather_data = [
        {"city_id": 1, "weather": "sunny"},
        {"city_id": 2, "weather": "rainy"},
        {"city_id": 3, "weather": "cloudy"},
    ]
    parsed_weather_data = [
        {"city_id": 1, "weather": "sunny"},
        {"city_id": 2, "weather": "rainy"},
        {"city_id": 3, "weather": "cloudy"},
    ]

    mock_fetch_all_weather_data.return_value = weather_data
    mock_parse_weather_data.side_effect = parsed_weather_data

    with patch("app.utils.fetch_all_weather_data", mock_fetch_all_weather_data), patch(
        "app.utils.parse_weather_data", mock_parse_weather_data
    ), patch("app.crud.create_weather_data", mock_create_weather_data), patch(
        "app.crud.update_request_log", mock_update_request_log
    ):

        result = await process_data(
            db=MagicMock(), city_ids=city_ids, request_log=request_log
        )

        assert result == request_log
        assert mock_fetch_all_weather_data.called
        assert mock_parse_weather_data.call_count == len(weather_data)
        assert mock_create_weather_data.call_count == len(weather_data)
        assert mock_update_request_log.call_count == len(weather_data)
        assert mock_update_request_log.call_args_list[0][1]["cities_collected"] == 1
        assert mock_update_request_log.call_args_list[1][1]["cities_collected"] == 2
        assert mock_update_request_log.call_args_list[2][1]["cities_collected"] == 3
