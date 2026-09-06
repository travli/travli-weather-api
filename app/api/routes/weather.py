from fastapi import APIRouter, Query

from app.schemas.weather import WeatherResponse
from app.services.weather_service import WeatherService


router = APIRouter(
    prefix="/api/v1/weather",
    tags=["weather"],
)

weather_service = WeatherService()


@router.get("", response_model=WeatherResponse)
async def get_weather(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
):
    return await weather_service.get_weather(
        latitude,
        longitude,
    )
