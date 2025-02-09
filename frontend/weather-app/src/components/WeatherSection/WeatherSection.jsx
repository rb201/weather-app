import { useEffect, useState } from "react";

export default function WeatherSection() {
  const [weatherData, setWeaatherData] = useState(null);

  const primaryData = {}
  const secondaryData = {}

  useEffect(() => {
    const fetchWeatherData = async () => {
      const res = await fetch("http://localhost:8000/current/");
      const currentWeatherData = await res.json();

      if (!res.ok) {
        throw new Error("Network response was not ok");
      }

      setWeaatherData(JSON.parse(currentWeatherData));
    };

    fetchWeatherData();
  }, []);

  function parseSecWeatherData() {
    secondaryData["Humidity"] = weatherData['humidity'];
    secondaryData["Wind"] = weatherData["wind_speed"],
    secondaryData["Pressure"] = weatherData["pressure"],
    secondaryData["Visibility"] = weatherData["visibility"],
    secondaryData["Sunset"] = weatherData["sunset"]
    secondaryData["Rain"] = weatherData["rain"]
  }


  if (weatherData) {
    // console.log(weatherData);
    parseSecWeatherData()
    console.log(secondaryData)
  }

  return (
    <>
        <div className="weather-container__current-secondary-infos">
            {Object.keys(secondaryData).map((key) => {
                return (<div className="weather-container__current-secondary-info">
                    <p key={key} className="weather-container__current-secondary-info-item">{key}</p>
                    <p key={key} className="weather-container__current-secondary-info-item">{secondaryData[key]}</p>
                </div>)
            })}
        </div>
    </>
  );
}
