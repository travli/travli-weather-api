from pydantic import BaseModel


class CurrentWeather(BaseModel):
    temperature: float
    wind_speed: float
    weather_code: int


class DailyWeather(BaseModel):
    date: str
    temperature_max: float
    temperature_min: float
    weather_code: int


class WeatherResponse(BaseModel):
    latitude: float
    longitude: float
    timezone: str
    current: CurrentWeather
    daily: list[DailyWeather]
