from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.data_fetcher import WeatherFetcher

origins = [
    "http://localhost:5173"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_methods = ["GET"]
)

@app.get("/health")
async def health_status():
    return {"message": "ok"}


@app.get("/current/")
async def get_current_weather(city: str, state: str):
    wf = WeatherFetcher("weather.db", city = city, state = state)
    current_weather_data = wf.get_current_weather()
    print(current_weather_data)

    return current_weather_data
