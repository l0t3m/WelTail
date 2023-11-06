function ShowPage(props) {
    const [dogBreeds, setDogBreeds] = React.useState({});

    React.useEffect(()=>{
        axios.get('https://dog.ceo/api/breeds/list/all').then((response)=>{
            setDogBreeds(response.data);
        });

    },[]);


    return (
        <div className="test">
            {dogBreeds.map((breed) => {
                <div>{breed}</div>
            })}
        </div>
    )
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<ShowPage/>);