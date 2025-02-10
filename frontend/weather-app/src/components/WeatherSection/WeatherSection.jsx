import { useEffect, useState } from "react";

import sunIcon from "../../assets/weather-icons/sun.png";


export default function WeatherSection() {
  const [ weatherData, setWeaatherData ] = useState(null);
  const [ isLoadingData, setIsLoadingData ] = useState(true);

  useEffect(() => {
    const fetchWeatherData = async () => {
        try {
            const res = await fetch("http://localhost:8000/current/");
            const currentWeatherData = await res.json();

            if (!res.ok) {
              throw new Error("Network response was not ok");
            }

            setWeaatherData(JSON.parse(currentWeatherData));
            setIsLoadingData(false)
        } catch (error) {
            console.log(error)
        }
    };

    fetchWeatherData();
  }, []);

  function parsePrimaryWeatherData() {
    if (isLoadingData) return <div>Loading...</div>

    const temperature = weatherData["temperature"];
    const apparent_temperature = weatherData["apparent_temperature"];
    const description = weatherData["forecast_main_description"];

    return (
      <div className="weather-container__current-primary-info">
        <p className="weather-container__current-main-location">Jersey City, NJ, USA</p>
        <img
          src={sunIcon}
          className="weather-container__current-logo"
          alt="sun"
        />
        <p className="weather-container__current-main-desc">{description}</p>
        <h2 className="weather-container__current-main-temp">{temperature}°C</h2>
        <p className="weather-container__current-main-feels-like">
          Feels like {apparent_temperature}°C
        </p>
      </div>
    );
  }

  function parseSecWeatherData() {
    if (isLoadingData) return <div>Loading...</div>

    const secondaryData = {};

    secondaryData["Humidity"] = weatherData["humidity"];
    secondaryData["Wind"] = weatherData["wind_speed"];
    secondaryData["Pressure"] = weatherData["pressure"];
    secondaryData["Visibility"] = weatherData["visibility"];
    secondaryData["Sunset"] = weatherData["sunset"];
    secondaryData["Rain"] = weatherData["rain"];

    return (
      <div className="weather-container__current-secondary-infos">
        {Object.keys(secondaryData).map((key, idx) => {
          return (
            <div key={idx} className="weather-container__current-secondary-info">
              <p key={key + "_key"}className="weather-container__current-secondary-info-item">{key}</p>
              <p key={key + "_val"} className="weather-container__current-secondary-info-item">{secondaryData[key]}</p>
            </div>
          );
        })}
      </div>
    );
  }

  return (
    <>
        {parsePrimaryWeatherData()}
        {parseSecWeatherData()}
    </>
  )
}
