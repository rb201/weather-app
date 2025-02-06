export default function Navigation(props) {
    return (
        <>
            <nav className="top-navigation">
                <search>
                    <form htmlFor="search" method="GET" className="form-search">
                        <div>
                            <input name="search" type="text" placeholder="City" /> 
                        </div>
                    </form>
                </search>
            </nav>
        </>
    )
}