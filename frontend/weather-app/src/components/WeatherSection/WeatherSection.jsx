import sunIcon from "../../assets/weather-icons/color/615.png";

import './WeatherSection.css'

export default function WeatherSection({ isLoadingData, weatherData }) {
  function parsePrimaryWeatherData() {
    if (isLoadingData) return <div>Loading...</div>

    const temperature = weatherData.data.temperature;
    const apparent_temperature = weatherData.data.apparent_temperature;
    const description = weatherData.data.forecast_main_description;

    return (
      <div className="weather-container__current-primary-info">
        <p className="weather-container__current-main-location">{weatherData.city}, {weatherData.state ? weatherData.state : weatherData.country}</p>
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

    secondaryData["Humidity"] = weatherData.data.humidity;
    secondaryData["Wind"] = weatherData.data.wind_speed;
    secondaryData["Pressure"] = weatherData.data.pressure;
    secondaryData["Visibility"] = weatherData.data.visibility;
    secondaryData["Sunset"] = weatherData.data.sunset;
    secondaryData["Rain"] = weatherData.data.rain;
    secondaryData["Snow"] = weatherData.data.snow;

    return (
      <div className="weather-container__current-secondary-infos">
        {Object.keys(secondaryData).map((key, idx) => {
          if (secondaryData[key] !== null) {
            return (
              <div key={idx} className="weather-container__current-secondary-info">
                <p key={key + "_key"}className="weather-container__current-secondary-info-item">{key}</p>
                <p key={key + "_val"} className="weather-container__current-secondary-info-item">{secondaryData[key]}</p>
              </div>
            );
          }
        })}
      </div>
    );
  }

  return (
    <>
        {parsePrimaryWeatherData()}
        {/* {parseSecWeatherData()} */}
    </>
  )
}
