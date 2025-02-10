import dotenv
import json
import os
import requests
import sqlite3
import sys

from contextlib import contextmanager
from geopy.geocoders import Nominatim

CWD = os.path.dirname(os.path.abspath(__file__))
ENV_FILE_PATH = os.path.join(CWD, ".env")

dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")

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
                    print(f"Error closing sql connection: {sqle}")
    

class WeatherFetcher:
    def __init__(
        self,
        db_path: str,
        latitude: float = None,
        longitude: float = None,
        city: str = None,
        state: str = None
    ):
        if longitude is None and latitude is None and city is None and state is None:
            print("Please include the coordinates of your location, or city and state")
            return

        self.db = DatabaseConnection(db_path)
        self.latitude = latitude
        self.longitude = longitude
        self.city = city
        self.state = state


    def add_city_to_db(
        self,
        name: str,
        state: str,
        country: str,
        timezone: str,
        latitude: float,
        longitude: float,
        hourly_url: str,
        forecast_url: str
    ) -> int:
        db_conn = self.db.get_connection()

        with db_conn as conn:
            try:
                cur = conn.cursor()

                add_city_query = (
                    """
                    INSERT INTO cities
                    (
                        name, state, country, timezone,
                        longitude, latitude, hourly_url, forecast_url
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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

                city_id = cur.lastrowid
            except sqlite3.Error as sqle:
                print(f"Error adding city to database.cities: {sqle}")

        return city_id


    def get_current_weather(self):
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.latitude}&lon={self.longitude}&units=metric&appid={API_KEY}"

        try:
            res = requests.get(url)
            res.raise_for_status()
        except requests.HTTPError as http_error:
            print(f"HTTP error: {http_error}")
        except Exception as err:
            print(f"Error has occured: {err}")

        # with open("owm_current.json", 'r') as f:
        #     res = json.load(f)

        current_weather_data = json.loads(res.text)
        print(current_weather_data)
        # current_weather_data = res
        parsed_current_weather_data = {
            "temperature": current_weather_data.get("main", {}).get("temp", None),
            "apparent_temperature": current_weather_data.get("main", {}).get("feels_like", None),
            "temperature_min": current_weather_data.get("main", {}).get("temp_min", None),
            "temperature_max": current_weather_data.get("main", {}).get("temp_max", None),
            "pressure": current_weather_data.get("main", {}).get("pressure", None),
            "humidity": current_weather_data.get("main", {}).get("humidity", None),
            "forecast_main_description": current_weather_data.get("weather", {})[0].get("main"),
            "forecast_short_description": current_weather_data.get("weather", {})[0].get("description"),
            "sunrise": current_weather_data.get("sys", {}).get("sunrise", None),
            "sunset": current_weather_data.get("sys", {}).get("sunset", None),
            "timestamp_calc": current_weather_data.get("dt", None),
            "wind_speed": current_weather_data.get("wind", {}).get("speed", None),
            "wind_direction": current_weather_data.get("wind", {}).get("deg", None),
            "wind_gust": current_weather_data.get("wind", {}).get("gust", None),
            "rain": current_weather_data.get("rain", None),
            "snow": current_weather_data.get("snow", None),
            "visibility": current_weather_data.get("visibility", None),
        }
        timezone = parsed_current_weather_data.get("timezone")

        if self.city is None and self.state is None:
            self.get_city_from_lon_lat()

        city_id = self.is_city_in_db()

        if not city_id:
            city_id = self.add_city_to_db(
                name = self.city,
                state = self.state,
                country = self.country,
                timezone = timezone,
                latitude = self.latitude,
                longitude = self.longitude,
                hourly_url = url,
                forecast_url = ""
            )

        self.write_current_weather_to_db(
            city_id = city_id,
            data = parsed_current_weather_data
        )


    def get_current_weather_from_db(self):
        info = [self.city, self.state]

        if not self.city and self.state:
            return {"message": "error, city and/or state not defined"}

        db_conn = self.db.get_connection()

        with db_conn as conn:
            try:
                cur = conn.cursor()

                query = """
                    SELECT hw.*
                    FROM hourly_weather hw
                    JOIN cities c on hw.city_id
                    WHERE name = ? and state = ?
                    ORDER BY hw.id DESC
                    LIMIT 1
                """

                query_data = cur.execute(query, info).fetchone()

            except sqlite3.Error as sqle:
                print(f"Error has occurred {sqle}")

        cur_weather_obj = {
            "temperature": query_data[2],
            "apparent_temperature": query_data[3],
            "temperature_min": query_data[4],
            "temperature_max": query_data[5],
            "pressure": query_data[6],
            "humidity": query_data[7],
            "forecast_main_description": query_data[8],
            "forecast_short_description": query_data[9],
            "sunrise": query_data[10],
            "sunset": query_data[11],
            "timestamp_calc": query_data[12],
            "wind_speed": query_data[13],
            "wind_direction": query_data[14],
            "wind_gust": query_data[15],
            "rain": query_data[16],
            "snow": query_data[17],
            "visibility": query_data[18]
        }

        return json.dumps(cur_weather_obj)

    def get_city_from_lon_lat(self):
        geolocater = Nominatim(user_agent = 'my-weather-app')

        location = geolocater.reverse(str(self.latitude) + ',' + str(self.longitude))

        self.city = location.raw['address']['city']
        self.state = location.raw['address']['state']
        self.country = location.raw['address']['country_code']
    
    
    def get_coor_from_city_state(self, city: str, state: str):
        # geolocater = Nominatim(user_agent = 'my-weather-app')
        pass


    def is_city_in_db(self) -> bool:
        db_conn = self.db.get_connection()

        info = [self.city, self.state]

        with db_conn as conn:
            try:
                cur = conn.cursor()
                
                query = (
                    """
                    SELECT id, name, state
                    FROM cities
                    WHERE name = ? and state = ?
                    """
                )

                cur.execute(query, info)

                city_in_db = cur.fetchone()
            except sqlite3.Error as sqle:
                print(f"Error has occured: {sqle}")

        return False if not city_in_db else city_in_db[0]

    def write_current_weather_to_db(self, city_id: int, data: dict):
        db_conn = self.db.get_connection()
        
        temperature = data["temperature"]
        apparent_temperature = data["apparent_temperature"]
        temperature_min = data["temperature_min"]
        temperature_max = data["temperature_max"]
        pressure = data["pressure"]
        humidity = data["humidity"]
        forecast_main_description = data["forecast_main_description"]
        forecast_short_description = data["forecast_short_description"]
        sunrise = data["sunrise"]
        sunset = data["sunset"]
        timestamp_calc = data["timestamp_calc"]
        wind_speed = data["wind_speed"]
        wind_direction = data["wind_direction"]
        wind_gust = data["wind_gust"]
        rain = data["rain"]
        snow = data["snow"]
        visibility = data["visibility"]
        
        parsed_data = [
            temperature, apparent_temperature, temperature_min, temperature_max, pressure,
            humidity, forecast_main_description, forecast_short_description, sunrise, sunset,
            timestamp_calc, wind_speed, wind_direction, wind_gust, rain, snow, visibility,
        ]

        with db_conn as conn:
            try:
                cur = conn.cursor()

                cur.execute(f"""
                    INSERT INTO hourly_weather (
                        city_id,
                        temperature,
                        apparent_temperature,
                        temperature_min,
                        temperature_max,
                        pressure,
                        humidity,
                        forecast_main_description,
                        forecast_short_description,
                        sunrise,
                        sunset,
                        timestamp_calc,
                        wind_speed,
                        wind_direction,
                        wind_gust,
                        rain,
                        snow,
                        visibility
                    )
                    VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                """, (city_id, *parsed_data))

                conn.commit()
            except sqlite3.Error as sqle:
                print(sqle)


# db_file = "weather.db"
# lat, long = 40.719074, -74.050552

# weather_obj = WeatherFetcher(db_file, longitude = long, latitude = lat)
# weather_obj.get_current_weather()
