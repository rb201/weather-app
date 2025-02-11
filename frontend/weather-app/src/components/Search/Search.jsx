export default function Search({ searchInput, setSearchInput }) {
    const searchInputHandler = (e) => {
        setSearchInput(e.target.value)
    }

    const submitFormHandler = async (e) => {
        e.preventDefault()

        const [ city, state ] = searchInput.split(',').map( word => word.trim())

        let urlParams = new URLSearchParams({city, state})

        try {
            const res = await fetch(`http://localhost:8000/search/?${urlParams}`)

            if (!res.ok) throw new Error('Submission failed');

        } catch (err) {
            throw new Error(`Error has occurred: ${err}`)
        }
    }

    return (
        <search>
            <form 
                htmlFor="search"
                method="GET"
                className="form-search"
                onSubmit={submitFormHandler}
            >
                <input 
                    name="search"
                    type="text"
                    placeholder="City, Country"
                    onChange={searchInputHandler}
                /> 
            </form>
        </search>
    )
}