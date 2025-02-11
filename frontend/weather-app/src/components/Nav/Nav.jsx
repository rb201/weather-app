import Search from '../Search/Search.jsx';

import './Nav.css';

export default function Navigation({ searchInput, setSearchInput }) {
    return (
        <>
            <nav className="top-navigation">
                <Search
                    searchInput={searchInput}
                    setSearchInput={setSearchInput}/>
                <button className="weather-container__current-title-bar-tenp-button">
                    C to F
                </button>
            </nav>
        </>
    )
}