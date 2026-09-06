from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "tavli-weather-api"
    app_env: str = "development"
    port: int = 8001

    open_meteo_base_url: str = "https://api.open-meteo.com/v1/forecast"

    redis_url: str = "redis://localhost:6379"
    redis_ttl: int = 3600

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
