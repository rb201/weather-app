import { useState } from "react";
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import "./App.css";

import Navigation from "./components/Nav/Nav";

import sunIcon from "./assets/weather-icons/sun.png";

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <div>
        <Navigation />
        {/* <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a> */}
      </div>
      <div className="weather-container__current">
        <div className="weather-alert">
          {/* <h3>alert</h3> */}
        </div>

        <div className="weather-container__current-title-bar">
          <h3 className="weather-container__current-title">Current Weather</h3>
          <button className="weather-container__current-title-bar-tenp-button">
            C to F
          </button>
        
        </div>
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
          <div className="weather-container__current-secondary-infos">
            <div className="weather-container__current-secondary-info">
              <p className="weather-container__current-secondary-info-item">
                Humidity
              </p>
              <p className="weather-container__current-secondary-info-item">
                73%
              </p>
            </div>
            <div>
              <p className="weather-container__current-secondary-info">Wind</p>
              <p className="weather-container__current-secondary-info">3</p>
            </div>
            <p className="weather-container__current-secondary-info">
              Pressure
            </p>
            <p className="weather-container__current-secondary-info">
              Visibility
            </p>
            <p className="weather-container__current-secondary-info">Sunset</p>
            <p className="weather-container__current-secondary-info">Rain</p>
            <p className="weather-container__current-secondary-info">Snow</p>
          </div>
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
