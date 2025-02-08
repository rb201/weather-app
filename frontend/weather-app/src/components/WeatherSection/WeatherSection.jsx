import { useEffect, useState } from "react";

export default function WeatherSection(props) {
  useEffect(() => {
    const fetchWeatherData = async () => {
      const res = await fetch("http://localhost:8000/current/");
      const currentWeatherData = await res.json()

    };

    fetchWeatherData()
  }, []);

  if (props.component === "secondary") {
    <div className="weather-container__current-secondary-infos"></div>;
  }

  return (
    <>
      <p>hey</p>
    </>
  );
}
