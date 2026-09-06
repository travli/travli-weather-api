import pytest

from app.providers.open_meteo import OpenMeteoProvider


class FakeResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {
            "latitude": 43.263,
            "longitude": -2.935,
            "timezone": "Europe/Madrid",
            "current": {
                "temperature_2m": 21.4,
                "wind_speed_10m": 12.3,
                "weather_code": 3,
            },
            "daily": {
                "time": ["2026-09-06"],
                "temperature_2m_max": [24.1],
                "temperature_2m_min": [16.2],
                "weather_code": [2],
            },
        }


class FakeAsyncClient:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def get(self, url, params, timeout):
        assert url == "https://api.open-meteo.com/v1/forecast"

        assert params["latitude"] == 43.263
        assert params["longitude"] == -2.935

        assert params["current"] == "temperature_2m,wind_speed_10m,weather_code"

        assert params["daily"] == "temperature_2m_max,temperature_2m_min,weather_code"

        assert params["timezone"] == "auto"
        assert timeout == 10

        return FakeResponse()


@pytest.mark.asyncio
async def test_open_meteo_get_weather(monkeypatch):
    monkeypatch.setattr(
        "app.providers.open_meteo.httpx.AsyncClient",
        lambda: FakeAsyncClient(),
    )

    provider = OpenMeteoProvider()

    result = await provider.get_weather(
        43.263,
        -2.935,
    )

    assert result["latitude"] == 43.263
    assert result["longitude"] == -2.935
    assert result["timezone"] == "Europe/Madrid"
    assert result["current"]["temperature_2m"] == 21.4
