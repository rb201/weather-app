import { useState } from 'react';

export default function Search() {
    const [ searchInput, setSearchInput ] = useState("")

    const searchInputHandler = (e) => {
        setSearchInput(e.target.value)
    }

    const submitFormHandler = async (e) => {
        e.preventDefault()

        let [ city, state ] = searchInput.split(',')

        let urlParams = new URLSearchParams({city, state})

        try {
            const res = await fetch(`http://localhost:8000/current/?${urlParams}`)
            // const wea
        } catch (err) {
            throw new Error(`Error has occurred: ${err}`)
        }
        console.log(searchInput)
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