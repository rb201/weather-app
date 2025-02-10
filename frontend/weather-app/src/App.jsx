import "./App.css";

import Navigation from "./components/Nav/Nav";
import WeatherSection from "./components/WeatherSection/WeatherSection";

function App() {
  return (
    <>
      <div>
        <Navigation />
      </div>
      <div className="weather-container__current">
        <div className="weather-alert">{/* <h3>alert</h3> */}</div>
        <div className="weather-container__current-main">
          <WeatherSection />
        </div>
        <div className="weather-container__hourly">
          <p>hourly</p>
        </div>
      </div>
    </>
  );
}

export default App;
