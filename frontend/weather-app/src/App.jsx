import { useState } from "react";
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import "./App.css";

import Navigation from "./components/Nav/Nav";
import WeatherSection from "./components/WeatherSection/WeatherSection";

import sunIcon from "./assets/weather-icons/sun.png";

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <div>
        <Navigation />

      </div>
      <div className="weather-container__current">
        <div className="weather-alert">{/* <h3>alert</h3> */}</div>
        <div className="weather-container__current-main">
          <div className="weather-container__current-primary-info">
            <p className="weather-container__current-main-location">
              Jersey City, NJ, USA
            </p>
            <img
              src={sunIcon}
              className="weather-container__current-logo"
              alt="sun"
            />
            <p className="weather-container__current-main-desc">Sunny</p>
            <h2 className="weather-container__current-main-temp">19°C</h2>
            <p className="weather-container__current-main-feels-like">
              Feels like 18°C
            </p>
          </div>
          <WeatherSection />

          {/* <div className="weather-container__current-secondary-infos">
            <div className="weather-container__current-secondary-info">
              <p className="weather-container__current-secondary-info-item">
                Humidity
              </p>
              <p className="weather-container__current-secondary-info-item">
                73%
              </p>
            </div>
            <div className="weather-container__current-secondary-info">
              <p className="weather-container__current-secondary-info-item">
                Wind
              </p>
              <p className="weather-container__current-secondary-info-item">
                3
              </p>
            </div>
            <div className="weather-container__current-secondary-info">
              <p className="weather-container__current-secondary-info-item">
                Pressure
              </p>
              <p className="weather-container__current-secondary-info-item">1013 hPa</p>
            </div>
            <div className="weather-container__current-secondary-info">
              <p className="weather-container__current-secondary-info-item">
                Visibility
              </p>
              <p className="weather-container__current-secondary-info-item">
                10km
              </p>
            </div>
            <div className="weather-container__current-secondary-info">
              <p className="weather-container__current-secondary-info-item">
                Sunset
              </p>
              <p className="weather-container__current-secondary-info-item">
                6:45pm
              </p>
            </div>
            <div className="weather-container__current-secondary-info">
              <p className="weather-container__current-secondary-info-item">Rain</p>
              <p className="weather-container__current-secondary-info-item">1 inch</p>
            </div>
          </div> */}
        </div>
        <div className="weather-container__hourly">
          <p>hourly</p>
        </div>
      </div>
      {/* <h1>Vite + React</h1> */}
      <div className="card">
        {/* <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button> */}
        {/* <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p> */}
      </div>
      {/* <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p> */}
    </>
  );
}

export default App;
