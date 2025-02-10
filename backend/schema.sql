DROP TABLE IF EXISTS cities;
DROP TABLE IF EXISTS hourly_weather;
DROP TABLE IF EXISTS forecast;

CREATE TABLE IF NOT EXISTS cities (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    state TEXT NOT NULL,
    country TEXT,
    longitude REAL NOT NULL,
    latitude REAL NOT NULL,
    timezone TEXT,
    hourly_url TEXT NOT NULL,
    forecast_url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS hourly_weather (
    id INTEGER PRIMARY KEY,
    city_id INTEGER NOT NULL,
    temperature INTEGER,
    apparent_temperature INTEGER,
    temperature_min INTEGER,
    temperature_max INTEGER,
    pressure INTEGER,
    humidity INTEGER,
    forecast_main_description TEXT,
    forecast_short_description TEXT,
    sunrise INTEGER,
    sunset INTEGER,
    timestamp_calc INT,
    wind_speed REAL,
    wind_direction INTEGER,
    wind_gust REAL,
    rain REAL,
    snow REAL,
    visibility INTEGER,
    FOREIGN KEY (city_id) REFERENCES cities(id)
);

-- CREATE TABLE IF NOT EXISTS forecast (
--     id INTEGER PRIMARY KEY,
--     city_id INTEGER NOT NULL,
--     time_of_day_desc TEXT,
--     start_time TEXT,
--     end_time TEXT,
--     temperature INTEGER,
--     termperature_unit TEXT,
--     precipitation_probability INTEGER,
--     rain REAL,
--     snow REAL,
--     wind_speed TEXT,
--     wind_direction TEXT,
--     forcast_short_desc TEXT,
--     forcast_long_desc TEXT,
--     FOREIGN KEY (city_id) REFERENCES cities(id)
-- );
