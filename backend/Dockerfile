FROM python:3.11-slim

WORKDIR /app

COPY . /app 

RUN pip install -r requirements.txt

ENTRYPOINT ["fastapi", "run", "--port", "8000", "api.py"]