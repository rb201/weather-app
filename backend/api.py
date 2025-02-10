from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from data_fetcher import WeatherFetcher

origins = [
    "http://localhost:5173"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_methods = ["GET"]
)

@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/health")
async def health_status():
    return {"message": "ya i'm ok"}


@app.get("/current/")
async def get_current_weather():
    city, state = "Jersey City", "New Jersey"
    
    wf = WeatherFetcher("weather.db", city = city, state = state)
    current_weather_data = wf.get_current_weather_from_db()

    return current_weather_data
