FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["fastapi", "run", "--port", "8000", "api.py"]