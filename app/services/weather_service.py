import json

from app.cache.redis import RedisCache
from app.providers.open_meteo import OpenMeteoProvider
from app.schemas.weather import (
    CurrentWeather,
    DailyWeather,
    WeatherResponse,
)


class WeatherService:
    def __init__(self):
        self.provider = OpenMeteoProvider()
        self.cache = RedisCache()

    async def get_weather(
        self,
        latitude: float,
        longitude: float,
    ) -> WeatherResponse:
        cache_key = f"weather:{latitude:.4f}:{longitude:.4f}"

        cached = await self.cache.get(cache_key)

        if cached:
            return WeatherResponse(**json.loads(cached))

        data = await self.provider.get_weather(
            latitude,
            longitude,
        )

        current_data = data["current"]
        daily_data = data["daily"]

        current = CurrentWeather(
            temperature=current_data["temperature_2m"],
            wind_speed=current_data["wind_speed_10m"],
            weather_code=current_data["weather_code"],
        )

        daily = [
            DailyWeather(
                date=daily_data["time"][index],
                temperature_max=(daily_data["temperature_2m_max"][index]),
                temperature_min=(daily_data["temperature_2m_min"][index]),
                weather_code=(daily_data["weather_code"][index]),
            )
            for index in range(len(daily_data["time"]))
        ]

        result = WeatherResponse(
            latitude=data["latitude"],
            longitude=data["longitude"],
            timezone=data["timezone"],
            current=current,
            daily=daily,
        )

        await self.cache.set(
            cache_key,
            json.dumps(result.model_dump()),
        )

        return result
