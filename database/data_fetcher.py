import json
import os
import sqlite3

from contextlib import contextmanager
from geopy.geocoders import Nominatim


class DatabaseConnection:
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    @contextmanager
    def get_connection(self):
        conn = None
        
        try:
            CWD = os.path.dirname(os.path.abspath(__file__))
            DATABASE = os.path.join(CWD, self.db_path)

            conn = sqlite3.connect(DATABASE)
            yield conn
        except sqlite3.Error as sqle:
            print(sqle)
            # raise
        finally:
            if conn:
                try:
                    conn.close()
                except sqlite3.Error as slqe:
                    print("Error closing sql connection")
    

class WeatherFetcher:
    def __init__(self, ):
        pass


    def get_current_weather(self, ):
        pass


    def get_forecast(self,):
        pass


    def get_historical_weather(self, ):
        pass

def get_db():
    # db = DatabaseConnection()
    pass

def if_city_in_db(city, state) -> bool:
    DATABASE = "weather.db"
    
    db = DatabaseConnection(DATABASE)
    
    with db.get_connection() as conn:
        try:
            cur = conn.cursor()
            
            query = (
                """
                SELECT name, state
                FROM cities 
                WHERE name = ? and state = ?
                """
            )
            
            cur.execute(query, (city, state))

            read_output = cur.fetchall()
            if not read_output:
                return False
            return True
                
        except sqlite3.Error as sqle:
            print(f"Error has occured: {sqle}")
            

def get_city_from_lon_lat(latitude: float, longitude: float):
    geolocater = Nominatim(user_agent = 'my-weather-app')
    
    location = geolocater.reverse(str(latitude) + ',' + str(longitude))
    
    print(location)
    print(location.raw['address'])
    city = location.raw['address']['city']
    state = location.raw['address']['state']
    return city, state


def add_city_to_db(
    name: str,
    state: str,
    country: str,
    timezone: str,
    longitude: float,
    latitude: float,
    hourly_url: str,
    forecast_url: str
):
    db = DatabaseConnection("weather.db")

    with db.get_connection() as conn:
        try:
            cur = conn.cursor()
            
            add_city_query = (
                """
                INSERT INTO cities
                (
                    name, state, country, timezone,
                    longitude, latitude, hourly_url, forecast_url
                )
                VALUES 
                (?, ?, ?, ?, ?, ?, ?, ?)
                """
            )
            
            cur.execute(
                add_city_query,
                (
                    name, state, country, timezone,
                    longitude, latitude, hourly_url, forecast_url
                )
            )
            
            conn.commit()
        except sqlite3.Error as sqle:
            print(f"Error adding city to database.cities: {sqle}")
            
        

def write_current_weather_to_db(data):
    DATABASE = "weather.db"
    
    temperature = data("temperature")
    apparent_temperature = data["apparent_temperature"]
    temperature_min = data["temperature_min"]
    temperature_max = data["temperature_max"]
    pressure = data["pressure"]
    humidty = data["humidity"]
    forecast_main_description = data["forecast_main_description"],
    forecast_short_description = data["forecast_short_description"],
    sunrise = data["sunrise"]
    sunset = data["sunset"]
    timestamp_calc = data["timestamp_calc"],
    wind_speed = data["wind_speed"],
    wind_gust = data["wind_gust"],
    rain = data["rain"],
    snow = data["snow"],
    visibility = data["visibility"],
    
    db = DatabaseConnection(DATABASE)
    
    with db.get_connection() as conn:
        try:
            cur = conn.cursor()
            
            cur.execute("""
                INSERT INTO hourly_weather (
                    city_id,
                    temperature,
                    apparent_temperature, 
                    temperature_min,
                    temperature_max,
                    pressure,
                    humidty,
                    forecast_main_description,
                    forecast_short_description,
                    sunrise,
                    sunset,
                    timestamp_calc,
                    wind_speed,
                    wind_gust,
                    rain,
                    snow,
                    visibility)
                VALUES (
                    (SELECT id FROM cities WHERE name = "Jersey CIty" and state = "NJ"), 
                    ?, ?, ?,
                    ?, ?, ?, ?,
                    ?, ?, ?, ?,
                    ?, ?, ?, ?, ?
                )
            """, data)
        
        except sqlite3.Error as sqle:
            print(sqle)


db_file = "weather.db"
# jc_forecast_file = "forcast.json"
# jc_forecast_hourly_file = "forcast_hourly.json"
jc_current_file = "owm_current.json"

# jcff = os.path.dirname()
# jcff = os.path.join(os.path.dirname('.'), jc_forecast_file)
# print(os.getcwd())
jcff = os.path.join(os.path.dirname('.'), jc_current_file)

with open(jcff, 'r') as f:
    data = json.load(f)
    
if not data:
    data = {}

# print(jc_forecast_data)
# jcf_start_time = data['weather']
parsed_data = {
    "temperature": data.get("main", {}).get("temp", None),
    "apparent_temperature": data.get("main", {}).get("feels_like", None),
    "temperature_min": data.get("main", {}).get("temp_min", None),
    "temperature_max": data.get("main", {}).get("temp_max", None),
    "pressure": data.get("main", {}).get("pressure", None),
    "humidty": data.get("main", {}).get("humidity", None),
    "forecast_main_description": data.get("weather", {})[0].get("main"),
    "forecast_short_description": data.get("weather", {})[0].get("description"),
    "sunrise": data.get("sys", {}).get("sunrise", None),
    "sunset": data.get("sys", {}).get("sunset", None),
    "timestamp_calc": data.get("dt", None),
    "wind_speed": data.get("wind", {}).get("speed", None),
    "wind_gust": data.get("wind", {}).get("gust", None),
    "rain": data.get("rain", None),
    "snow": data.get("snow", None),
    "visibility": data.get("visibility", None),
}

# print(jcf_start_time)
# write_to_db(parsed_data)
latitude = 40.719074
longitude = -74.050552
country = "US"
# city, state = get_city_from_lon_lat(lat, lon)
city = "Jersey City"
state = "New Jersey"

city_in_db = if_city_in_db(city, state)

if not city_in_db:
    add_city_to_db(
        name = city,
        state = state,
        country = country,
        longitude = longitude,
        latitude = latitude,
        timezone = "5gmt",
        hourly_url = "https://example.com/hourly",
        forecast_url = "https://example.com/forecast"
    )