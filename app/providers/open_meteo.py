import httpx

from app.config import settings


class OpenMeteoProvider:
    async def get_weather(
        self,
        latitude: float,
        longitude: float,
    ) -> dict:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,wind_speed_10m,weather_code",
            "daily": ("temperature_2m_max,temperature_2m_min,weather_code"),
            "timezone": "auto",
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                settings.open_meteo_base_url,
                params=params,
                timeout=10,
            )

        response.raise_for_status()

        return response.json()
