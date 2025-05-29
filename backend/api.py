from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import generate_latest, CollectorRegistry, Counter, Gauge

from .data_fetcher import WeatherFetcher

origins = ["http://*:3000"]

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["GET"])

metrics_registry = CollectorRegistry()

active_http_requests = Gauge(
    name="active_http_requests",
    documentation="Current active HTTP requests",
    registry=metrics_registry,
)

http_requests_total = Counter(
    name="http_requests_total",
    documentation="Total number of HTTP requests received",
    registry=metrics_registry,
    labelnames=["return_status", "route", "method"],
)


async def http_requests_metrics(request: Request):
    active_http_requests.inc()

    http_requests_total.labels(
        return_status=str(200), route=request.url.components.path, method=request.method
    ).inc()

    yield

    active_http_requests.dec()


@app.get("/current/")
async def get_current_weather(
    city: str, state: str, dep: str = Depends(http_requests_metrics)
):
    wf = WeatherFetcher("weather.db", city=city, state=state)
    current_weather_data = wf.get_current_weather()
    print(current_weather_data)

    return current_weather_data


@app.get("/health")
async def health_status(dep: str = Depends(http_requests_metrics)):
    return {"service": "ok"}


@app.get("/metrics")
def metrics():
    return generate_latest(metrics_registry).decode("utf8").split("\n")
