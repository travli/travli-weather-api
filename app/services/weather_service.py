from app.providers.open_meteo import OpenMeteoProvider
from app.schemas.weather import (
    CurrentWeather,
    DailyWeather,
    WeatherResponse,
)


class WeatherService:
    def __init__(self):
        self.provider = OpenMeteoProvider()

    async def get_weather(
        self,
        latitude: float,
        longitude: float,
    ) -> WeatherResponse:
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
                temperature_max=daily_data["temperature_2m_max"][index],
                temperature_min=daily_data["temperature_2m_min"][index],
                weather_code=daily_data["weather_code"][index],
            )
            for index in range(len(daily_data["time"]))
        ]

        return WeatherResponse(
            latitude=data["latitude"],
            longitude=data["longitude"],
            timezone=data["timezone"],
            current=current,
            daily=daily,
        )
