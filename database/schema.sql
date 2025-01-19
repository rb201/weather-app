-- DROP TABLE IF EXISTS cities
-- DROP TABLE IF EXISTS hourly_weather
-- DROP TABLE IF EXISTS forecast

CREATE TABLE cities (
    name TEXT NOT NULL,
    state TEXT NOT NULL,
    timezone TEXT,
    period_of_day TEXT,
    time_period,
    forecast_url TEXT NOT NULL,
    hourly_url TEXT NOT NULL,
    coordinates TEXT 
)

CREATE TABLE hourly_weather (
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    termperature INTEGER,
    termperature_unit TEXT,
    precipitation_probability INTEGER,
    dewpoint REAL,
    humidity INTEGER,
    wind_speed TEXT,
    wind_direction TEXT,
    forcast_short_desc TEXT,
)

CREATE TABLE forecast (
    time_of_day_desc TEXT,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    temperature INTEGER NOT NULL,
    termperature_unit TEXT NOT NULL,
    precipitation_probability INTEGER,
    wind_speed TEXT,
    wind_direction TEXT,
    forcast_short_desc TEXT,
    forcast_long_desc TEXT,
)