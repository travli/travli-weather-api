import json

import pytest

from app.services.weather_service import WeatherService


class FakeCache:
    def __init__(self, cached=None):
        self.cached = cached
        self.saved = None

    async def get(self, key):
        return self.cached

    async def set(self, key, value):
        self.saved = {
            "key": key,
            "value": value,
        }


class FakeProvider:
    def __init__(self):
        self.called = False

    async def get_weather(self, latitude, longitude):
        self.called = True

        return {
            "latitude": latitude,
            "longitude": longitude,
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


@pytest.mark.asyncio
async def test_get_weather_uses_cache():
    cached_data = json.dumps(
        {
            "latitude": 43.263,
            "longitude": -2.935,
            "timezone": "Europe/Madrid",
            "current": {
                "temperature": 21.4,
                "wind_speed": 12.3,
                "weather_code": 3,
            },
            "daily": [
                {
                    "date": "2026-09-06",
                    "temperature_max": 24.1,
                    "temperature_min": 16.2,
                    "weather_code": 2,
                }
            ],
        }
    )

    service = WeatherService()

    cache = FakeCache(cached=cached_data)
    provider = FakeProvider()

    service.cache = cache
    service.provider = provider

    result = await service.get_weather(43.263, -2.935)

    assert result.current.temperature == 21.4
    assert result.daily[0].date == "2026-09-06"

    assert provider.called is False


@pytest.mark.asyncio
async def test_get_weather_calls_provider_when_cache_is_empty():
    service = WeatherService()

    cache = FakeCache()
    provider = FakeProvider()

    service.cache = cache
    service.provider = provider

    result = await service.get_weather(43.263, -2.935)

    assert result.current.temperature == 21.4
    assert result.current.wind_speed == 12.3

    assert provider.called is True
    assert cache.saved is not None
    assert cache.saved["key"] == "weather:43.2630:-2.9350"


@pytest.mark.asyncio
async def test_get_weather_transforms_provider_response():
    service = WeatherService()

    service.cache = FakeCache()
    service.provider = FakeProvider()

    result = await service.get_weather(43.263, -2.935)

    assert result.latitude == 43.263
    assert result.longitude == -2.935
    assert result.timezone == "Europe/Madrid"

    assert result.current.temperature == 21.4
    assert result.current.wind_speed == 12.3
    assert result.current.weather_code == 3

    assert len(result.daily) == 1
    assert result.daily[0].temperature_max == 24.1
    assert result.daily[0].temperature_min == 16.2
    assert result.daily[0].weather_code == 2
