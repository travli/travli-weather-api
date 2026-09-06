# Travli Weather API

Weather microservice for **Travli**.

This service provides current and daily weather information using **Open-Meteo** as the external weather provider and **Redis** as a cache to reduce external API requests.

## Architecture

```text
                  ┌─────────────────────┐
                  │  Travli Weather API │
                  │       FastAPI       │
                  └──────┬────────┬─────┘
                         │        │
                    Cache hit     │ Cache miss
                         │        │
                         ▼        ▼
                      Redis    Open-Meteo
                         │        │
                         │        ▼
                         │    Store result
                         │        │
                         └────────┘
                             │
                             ▼
                         Response
```

## Features

* Current weather information
* Daily weather forecast
* Coordinate-based weather queries
* Automatic timezone detection
* Redis caching
* 1-hour cache expiration
* REST API with FastAPI
* OpenAPI documentation
* Unit and integration tests
* Docker support

## Technology Stack

* Python 3.12
* FastAPI
* Pydantic
* HTTPX
* Redis
* Open-Meteo
* pytest
* uv
* Docker

## Project Structure

```text
Travli-weather-api/
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── weather.py
│   ├── cache/
│   │   └── redis.py
│   ├── providers/
│   │   └── open_meteo.py
│   ├── schemas/
│   │   └── weather.py
│   ├── services/
│   │   └── weather_service.py
│   ├── config.py
│   └── main.py
│
├── tests/
│   ├── test_health.py
│   ├── test_weather.py
│   ├── test_weather_service.py
│   ├── test_open_meteo.py
│   └── test_redis.py
│
├── insomnia/
│   └── Travli-weather-api.json
│
├── .env.example
├── .gitignore
├── Dockerfile
├── pyproject.toml
├── uv.lock
└── README.md
```

## Requirements

* Python 3.12
* uv
* Docker
* Travli infrastructure with Redis

## Configuration

Create a `.env` file based on `.env.example`:

```env
APP_NAME=Travli-weather-api
APP_ENV=development
PORT=8001

OPEN_METEO_BASE_URL=https://api.open-meteo.com/v1/forecast

REDIS_URL=redis://localhost:6379
REDIS_TTL=3600
```

### Environment variables

| Variable              | Description               | Default                      |
| --------------------- | ------------------------- | ---------------------------- |
| `APP_NAME`            | Application name          | `Travli-weather-api`          |
| `APP_ENV`             | Application environment   | `development`                |
| `PORT`                | API port                  | `8001`                       |
| `OPEN_METEO_BASE_URL` | Open-Meteo API endpoint   | Open-Meteo forecast endpoint |
| `REDIS_URL`           | Redis connection URL      | `redis://localhost:6379`     |
| `REDIS_TTL`           | Cache lifetime in seconds | `3600`                       |

The `.env` file must not be committed to the repository.

## Installation

Install dependencies with:

```bash
uv sync
```

## Running locally

Make sure the Weather Redis instance from `Travli-infra` is running on port `6379`.

Start the API:

```bash
uv run uvicorn app.main:app --reload --port 8001
```

The API will be available at:

```text
http://localhost:8001
```

## API Documentation

Swagger UI:

```text
http://localhost:8001/docs
```

ReDoc:

```text
http://localhost:8001/redoc
```

## API Endpoints

### Health check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

### Get weather

```http
GET /api/v1/weather?latitude={latitude}&longitude={longitude}
```

Example:

```http
GET /api/v1/weather?latitude=43.263&longitude=-2.935
```

Example response:

```json
{
  "latitude": 43.263,
  "longitude": -2.935,
  "timezone": "Europe/Madrid",
  "current": {
    "temperature": 21.4,
    "wind_speed": 12.3,
    "weather_code": 3
  },
  "daily": [
    {
      "date": "2026-09-06",
      "temperature_max": 24.1,
      "temperature_min": 16.2,
      "weather_code": 2
    }
  ]
}
```

The API exposes a normalized Travli response instead of returning the raw Open-Meteo response.

## Caching

Weather data is cached in Redis for one hour.

The cache key uses the requested coordinates:

```text
weather:{latitude}:{longitude}
```

Example:

```text
weather:43.2630:-2.9350
```

The default TTL is:

```text
3600 seconds
```

The request flow is:

```text
Request
   │
   ▼
 Redis
   │
   ├── Cache hit ──────► Return cached data
   │
   └── Cache miss
            │
            ▼
        Open-Meteo
            │
            ▼
       Store in Redis
            │
            ▼
       Return response
```

## Testing

Run the complete test suite:

```bash
uv run pytest
```

Run Ruff:

```bash
uv run ruff check .
```

The test suite covers:

* Health endpoint
* Weather endpoint
* Latitude validation
* Longitude validation
* Weather service
* Cache hit behaviour
* Cache miss behaviour
* Open-Meteo provider
* Redis cache

External services are mocked during testing, so the tests do not require requests to Open-Meteo or a running Redis instance.

## Docker

Build the image:

```bash
docker build -t Travli-weather-api .
```

Run the container:

```bash
docker run --rm \
  --env-file .env \
  -p 8001:8001 \
  Travli-weather-api
```

When running the API inside Docker, `REDIS_URL` must reference a Redis service reachable from the container. `localhost` refers to the API container itself.

## Insomnia

An Insomnia workspace export is included in:

```text
insomnia/Travli-weather-api.json
```

Import the file into Insomnia to obtain:

```text
Travli Weather API
├── Health
└── Get Weather - Bilbao
```

The default environment uses:

```text
base_url = http://localhost:8001
```

## External Provider

The service uses **Open-Meteo** for weather data.

The provider implementation is isolated in:

```text
app/providers/open_meteo.py
```

This keeps the application independent from the external provider implementation and makes it possible to replace the provider without changing the API contract.

## Development

Start the development server:

```bash
uv run uvicorn app.main:app --reload --port 8001
```

Run tests:

```bash
uv run pytest
```

Run linting:

```bash
uv run ruff check .
```
