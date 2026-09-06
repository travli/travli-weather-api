from fastapi.testclient import TestClient

from app.api.routes.weather import weather_service
from app.main import app
from app.schemas.weather import (
    CurrentWeather,
    DailyWeather,
    WeatherResponse,
)

client = TestClient(app)


async def mock_get_weather(
    latitude: float,
    longitude: float,
) -> WeatherResponse:
    return WeatherResponse(
        latitude=latitude,
        longitude=longitude,
        timezone="Europe/Madrid",
        current=CurrentWeather(
            temperature=21.4,
            wind_speed=12.3,
            weather_code=3,
        ),
        daily=[
            DailyWeather(
                date="2026-09-06",
                temperature_max=24.1,
                temperature_min=16.2,
                weather_code=2,
            )
        ],
    )


def test_get_weather(monkeypatch):
    monkeypatch.setattr(
        weather_service,
        "get_weather",
        mock_get_weather,
    )

    response = client.get(
        "/api/v1/weather",
        params={
            "latitude": 43.263,
            "longitude": -2.935,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["latitude"] == 43.263
    assert data["longitude"] == -2.935
    assert data["timezone"] == "Europe/Madrid"

    assert data["current"]["temperature"] == 21.4
    assert data["current"]["wind_speed"] == 12.3
    assert data["current"]["weather_code"] == 3

    assert len(data["daily"]) == 1
    assert data["daily"][0]["date"] == "2026-09-06"


def test_get_weather_invalid_latitude():
    response = client.get(
        "/api/v1/weather",
        params={
            "latitude": 100,
            "longitude": -2.935,
        },
    )

    assert response.status_code == 422


def test_get_weather_invalid_longitude():
    response = client.get(
        "/api/v1/weather",
        params={
            "latitude": 43.263,
            "longitude": 200,
        },
    )

    assert response.status_code == 422
