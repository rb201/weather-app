import "./Search.css"

export default function Search({ searchInput, setSearchInput, setWeatherData, setIsLoadingData }) {
    const searchInputHandler = (e) => {
        setSearchInput(e.target.value)
    }

    const submitFormHandler = (e) => {
        e.preventDefault()
        fetchWeatherData()
    }

    const fetchWeatherData = async () => {
        console.log("In the fetch data function")
        const [ city, state ] = searchInput.split(',').map( word => word.trim())

        let urlParams = new URLSearchParams({city, state})

        try {
            console.log("In the try block for fetching data")
            const res = await fetch(`/api/current/?${urlParams}`);
            const currentWeatherData = await res.json();

            if (!res.ok) {
              throw new Error("Network response was not ok");
            }

            setWeatherData(JSON.parse(currentWeatherData));
            setIsLoadingData(false)
        } catch (error) {
            console.log(error)
        }
    };

    return (
        <search>
            <form 
                htmlFor="search"
                method="GET"
                className="form-search"
                onSubmit={submitFormHandler}
            >
                <input 
                    className="search-location"
                    name="search"
                    type="text"
                    placeholder="City, Country"
                    onChange={searchInputHandler}
                /> 
            </form>
        </search>
    )
}