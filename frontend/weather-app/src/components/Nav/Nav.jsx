import './Nav.css'

export default function Navigation(props) {
    return (
        <>
            <nav className="top-navigation">
                <search>
                    <form htmlFor="search" method="GET" className="form-search">
                        <input name="search" type="text" placeholder="City" /> 
                    </form>
                </search>
                <button className="weather-container__current-title-bar-tenp-button">
                    C to F
                </button>
            </nav>
        </>
    )
}