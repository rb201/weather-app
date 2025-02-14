import sunIcon from "../../assets/weather-icons/sun.png";

export default function WeatherSection({ isLoadingData, searchInput, weatherData}) {

  function parsePrimaryWeatherData() {
    if (isLoadingData) return <div>Loading...</div>

    const temperature = weatherData["temperature"];
    const apparent_temperature = weatherData["apparent_temperature"];
    const description = weatherData["forecast_main_description"];

    return (
      <div className="weather-container__current-primary-info">
        <p className="weather-container__current-main-location">Jersey City, NJ</p>
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
