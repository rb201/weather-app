import Search from '../Search/Search.jsx'

import './Nav.css'

export default function Navigation(props) {
    return (
        <>
            <nav className="top-navigation">
                <Search />
                <button className="weather-container__current-title-bar-tenp-button">
                    C to F
                </button>
            </nav>
        </>
    )
}