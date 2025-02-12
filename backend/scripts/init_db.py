import json
import os
import sqlite3

from contextlib import contextmanager

CWD = os.path.dirname(os.path.abspath("backend"))
DATABASE = os.path.join(CWD, "backend/weather.db")
SCHEMA_FILE = os.path.join(CWD, "backend/schema.sql")

GLOBAL_CITY_FILE = os.path.join(CWD, "backend/data/global_city.json")


@contextmanager
def db_connection(database: str):
    conn = None

    try:
        conn = sqlite3.connect(DATABASE)
        yield conn
    except sqlite3.Error as sqle:
        print(sqle)
    finally:
        if conn:
            try:
                conn.close()
            except sqlite3.Error as sqle:
                print("Error closing sql connection")


def populate_global_city_into_db(file):
    try:
        with open(file, "r") as f:
            global_city_data = json.load(f)
    except FileNotFoundError as fnfe:
        print(fnfe)

    with db_connection(DATABASE) as conn:
        cur = conn.cursor()

        for loc_obj in global_city_data:
            location_id = loc_obj["id"]
            city_name = loc_obj["name"]
            country_code = loc_obj["country"]
            longitude = loc_obj["coord"]["lon"]
            latitude = loc_obj["coord"]["lat"]

            location_info = [
                location_id, city_name, country_code, longitude, latitude
            ]

            query = """
                INSERT INTO global_list_of_cities (
                    location_id,
                    city_name,
                    country_code,
                    longitude,
                    latitude
                )
                VALUES (
                    ?, ?, ?, ?, ?
                )
            """

            cur.execute(
                query, [*location_info]
            )

            conn.commit()


def setup_tables():
    try:
        with open(SCHEMA_FILE, 'r') as sf:
            SQL_QUERY = sf.read()

    except FileNotFoundError as fnfe:
        raise fnfe

    db_conn = db_connection(DATABASE)

    with db_conn as conn:
        try:
            cur = conn.cursor()
            cur.executescript(SQL_QUERY)
        except sqlite3.Error as err:
            print(err)


# setup_tables()

populate_global_city_into_db(GLOBAL_CITY_FILE)