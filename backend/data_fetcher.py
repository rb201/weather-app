import dotenv
import json
import os
import requests
import sqlite3
import time

from typing import Optional, Tuple, Union

from .database_connection import DatabaseConnection

CWD = os.path.dirname(os.path.abspath(__file__))
ENV_FILE_PATH = os.path.join(CWD, ".env")

dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")


class WeatherFetcher:
    def __init__(
        self,
        db_path: str,
        city: str,
        state: str,
        country: str = "",
        latitude: Optional[float] = None,  # not supported yet
        longitude: Optional[float] = None,  # not supported yet
        location_id: Optional[int] = None,
    ):
        # if longitude is None and latitude is None and city is None and state is None:
        if city is None and state is None:
            # print("Please include the coordinates of your location, or city and state")
            print(
                "Validate your location, 'city, state' for USA. 'city, country' otherwise"
            )
            return

        self.db = DatabaseConnection(db_path)
        self.city = city
        self.state = state
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        self.location_id = location_id
        self.current_weather_url = f"https://api.openweathermap.org/data/2.5/weather?id={self.location_id}&units=metric&appid=API_KEY"

        if city and state:
            self.city, self.state, self.country, self.location_id = (
                self.validate_str_location(city=city, state=state)
            )
            print(
                f"found location id for {self.city}, {self.state}, {self.country}: {self.location_id}"
            )

            if self.location_id is None:
                raise Exception(
                    f"Can't find location. city: {self.city}, state: {self.state}"
                )

    def add_city_to_db(
        self,
        city: str,
        state: str,
        country: str,
        timezone: str,
        latitude: Union[float, None],
        longitude: Union[float, None],
        current_url: str,
        hourly_url: str,
    ) -> int:
        db_conn = self.db.get_connection()

        with db_conn as conn:
            try:
                cur = conn.cursor()

                add_city_query = """
                    INSERT INTO cities
                    (
                        name, state, country, timezone,
                        longitude, latitude, current_url, hourly_url
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """

                cur.execute(
                    add_city_query,
                    (
                        city,
                        state,
                        country,
                        timezone,
                        longitude,
                        latitude,
                        current_url,
                        hourly_url,
                    ),
                )

                conn.commit()

                city_id = cur.lastrowid
            except sqlite3.Error as sqle:
                print(f"Error adding city to database. {sqle}")

        return city_id

    def fetch_latest_current_weather_from_source(self) -> dict:
        url = f"https://api.openweathermap.org/data/2.5/weather?id={self.location_id}&units=metric&appid={API_KEY}"

        try:
            res = requests.get(url)
            res.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            print(f"HTTP error: {http_error}")
        except Exception as err:
            print(f"Error has occured: {err}")

        current_weather_data = json.loads(res.text)

        parsed_current_weather_data = {
            "weather_code": current_weather_data.get("weather", {})[0].get("id"),
            "temperature": current_weather_data.get("main", {}).get("temp", None),
            "apparent_temperature": current_weather_data.get("main", {}).get(
                "feels_like", None
            ),
            "temperature_min": current_weather_data.get("main", {}).get(
                "temp_min", None
            ),
            "temperature_max": current_weather_data.get("main", {}).get(
                "temp_max", None
            ),
            "clouds": current_weather_data.get("clouds", {}).get("all", None),
            "pressure": current_weather_data.get("main", {}).get("pressure", None),
            "humidity": current_weather_data.get("main", {}).get("humidity", None),
            "forecast_main_description": current_weather_data.get("weather", {})[0].get(
                "main", None
            ),
            "forecast_short_description": current_weather_data.get("weather", {})[
                0
            ].get("description", None),
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

        return parsed_current_weather_data

    def get_current_weather(self) -> str:
        def get_latest_data_and_write_to_db(city_id: int):
            latest_weather_data = self.fetch_latest_current_weather_from_source()

            self.write_current_weather_to_db(city_id=city_id, data=latest_weather_data)

        city_id = self.is_city_in_db()

        # If city doesnt exist in DB
        if city_id is None:
            city_id = self.add_city_to_db(
                city=self.city,
                state=self.state,
                country=self.country,
                timezone="",
                latitude=self.latitude,
                longitude=self.longitude,
                current_url=self.current_weather_url,
                hourly_url="",
            )

            get_latest_data_and_write_to_db(city_id)

        # Check if data is stale by looking at timestamp
        cur_weather_from_db = self.get_current_weather_from_db()
        cur_weather_timestamp = cur_weather_from_db["data"]["timestamp_calc"]

        # If data is older than 6hrs, get latest from api
        cur_time = int(time.time())
        if (cur_time - cur_weather_timestamp) > 21600:
            get_latest_data_and_write_to_db(city_id)

            return json.dumps(self.get_current_weather_from_db())

        return json.dumps(cur_weather_from_db)

    def get_current_weather_from_db(self) -> dict:
        loc_info = [self.city, self.state, self.country]

        db_conn = self.db.get_connection()

        with db_conn as conn:
            try:
                cur = conn.cursor()

                query = """
                    SELECT cw.*
                    FROM current_weather cw
                    JOIN cities c on cw.city_id == c.id
                    WHERE c.name = ? and c.state = ? and c.country = ?
                    ORDER BY cw.timestamp_calc DESC
                    LIMIT 1
                """

                query_data = cur.execute(query, loc_info).fetchone()

            except sqlite3.Error as sqle:
                print(f"Error has occurred {sqle}")

        cur_weather_obj = {
            "weather_code": query_data[2],
            "temperature": round(query_data[3], 1),
            "apparent_temperature": round(query_data[4], 1),
            "temperature_min": round(query_data[5], 1),
            "temperature_max": round(query_data[6], 1),
            "clouds": query_data[7],
            "pressure": str(query_data[8]) + " hPa",
            "humidity": str(query_data[9]) + "%",
            "forecast_main_description": query_data[10],
            "forecast_short_description": query_data[11],
            "sunrise": time.strftime("%H:%M:%S", time.localtime(query_data[12])),
            "sunset": time.strftime("%H:%M:%S", time.localtime(query_data[13])),
            "timestamp_calc": query_data[14],
            "wind_speed": query_data[15],
            "wind_direction": query_data[16],
            "wind_gust": query_data[17],
            "rain": query_data[18],
            "snow": query_data[19],
            "visibility": query_data[20],
        }

        data = {
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "data": cur_weather_obj,
        }

        return data

    # Returns city_id if city exists in db, None if it doesnt
    def is_city_in_db(self) -> Union[int, None]:
        db_conn = self.db.get_connection()

        info = [self.city, self.state, self.country]

        with db_conn as conn:
            try:
                cur = conn.cursor()

                query = """
                    SELECT id, name, state
                    FROM cities
                    WHERE name = ? and state = ? and country = ?
                    """

                cur.execute(query, info)

                city_in_db = cur.fetchone()
            except sqlite3.Error as sqle:
                print(f"Error has occured: {sqle}")

        return None if city_in_db is None else city_in_db[0]

    def write_current_weather_to_db(self, city_id: int, data: dict) -> None:
        db_conn = self.db.get_connection()

        weather_code = data["weather_code"]
        temperature = data["temperature"]
        apparent_temperature = data["apparent_temperature"]
        temperature_min = data["temperature_min"]
        temperature_max = data["temperature_max"]
        clouds = data["clouds"]
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
            weather_code,
            temperature,
            apparent_temperature,
            temperature_min,
            temperature_max,
            clouds,
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
            visibility,
        ]

        with db_conn as conn:
            try:
                cur = conn.cursor()

                cur.execute(
                    """
                    INSERT INTO current_weather (
                        city_id,
                        weather_code,
                        temperature,
                        apparent_temperature,
                        temperature_min,
                        temperature_max,
                        clouds,
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
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                    """,
                    (city_id, *parsed_data),
                )

                conn.commit()
            except sqlite3.Error as sqle:
                print(sqle)

    def load_json_data(self, file: str) -> dict:
        try:
            with open(CWD + file, "r") as f:
                return json.load(f)
        except FileNotFoundError as fnfe:
            print(f"{fnfe}")

        return {}

    # state is set to "" in db where city is not in the US
    def get_location_id_from_db(self, city, state, country) -> Union[int, None]:
        with self.db.get_connection() as db_conn:
            try:
                cur = db_conn.cursor()

                query = """
                    SELECT location_id
                    FROM global_list_of_cities
                    WHERE city_name = ? and state = ? and country_code = ?
                """

                cur.execute(query, [city, state, country])

                location_id = cur.fetchone()

                if location_id:
                    return location_id[0]

            except sqlite3.Error as sqle:
                print(sqle)

            return None

    def validate_str_location(
        self, city: str, state: str
    ) -> Tuple[str, str, str, Union[int, None]]:
        us_statecode_to_state_data = self.load_json_data(
            "/data/us_statecode_to_state_map.json"
        )
        us_state_to_statecode_map = self.load_json_data(
            "/data/us_state_to_statecode_map.json"
        )
        country_code_data = self.load_json_data("/data/country_code.json")

        city = city.lower().title()

        if len(state) == 2:
            state = state.upper()

            if state in us_statecode_to_state_data:
                country = "US"

                location_id = self.get_location_id_from_db(
                    city=city, state=state, country=country
                )

                return city, state, country, location_id

            country = state
            state = ""

            location_id = self.get_location_id_from_db(
                city=city, state=state, country=country
            )

            return city, state, country, location_id

        elif len(state) > 2:
            state = state.lower().title()

            if state in us_state_to_statecode_map:
                state = us_state_to_statecode_map[state]
                country = "US"

                location_id = self.get_location_id_from_db(
                    city=city, state=state, country=country
                )

                if location_id is None:
                    print(f"city: {city}, country {country} doesnt exist")
                    return city, state, "", None

                return city, state, country, location_id

            elif country_code_data.get(state, None):
                country = country_code_data[state]
                state = ""

                location_id = self.get_location_id_from_db(
                    city=city, state=state, country=country
                )

                if location_id is None:
                    print(f"city: {city}, country {country} doesnt exist")
                    return city, state, "", None

                return city, state, country, location_id

        print(f"Having trouble finding the state: {state}")
        return city, state, "", None


# db_file = "weather.db"
# lat, long = 40.719074, -74.050552

# weather_obj = WeatherFetcher(db_file, longitude = long, latitude = lat)
# weather_obj.get_current_weather()

test = ""
