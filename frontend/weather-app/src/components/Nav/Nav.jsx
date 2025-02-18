import Search from '../Search/Search.jsx';

import './Nav.css';

export default function Navigation({ searchInput, setIsLoadingData, setSearchInput, setWeatherData }) {
    return (
        <>
            <nav className="top-navigation">
                <Search
                    searchInput={searchInput}
                    setSearchInput={setSearchInput}
                    setWeatherData={setWeatherData}
                    setIsLoadingData={setIsLoadingData}
                />
                <button className="weather-container__current-title-bar-tenp-button">
                    C to F
                </button>
            </nav>
        </>
    )
}