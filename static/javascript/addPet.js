function ShowPage(props) {
    const [myUser, setMyUser] = React.useState("");

    React.useEffect(()=>{
        axios.get('/api/myUser').then((response)=>{
            setMyUser(response.data);
        });

    },[]);


    return (
        <div className="container rootContainer">

            <div className="header">Add a new pet</div>

            <form action={`/pet/add/${myUser.user_id}`} method="post">

                <div className="field flex">
                    <div>Type of pet</div>

                    <input type="radio" name="species" value="dog"/>
                    <div>Dog</div>

                    <input type="radio" name="species" value="cat"/>
                    <div>Cat</div>
                </div>

                <div className="field">
                    <div>Name</div>
                    <input type="text" name="name" placeholder="Name"/>
                </div>

                <div className="field flex">
                    <div>Gender</div>
                    <input type="radio" name="gender" value="male"/>
                    <div>Male</div>

                    <input type="radio" name="gender" value="female"/>
                    <div>Female</div>
                </div>

                <div className="field">
                    <div>Date of birth</div>
                    <input type="date" name="birthDate" placeholder="Birth Date"/>
                </div>

                <div className="field">
                    <div>Race</div>
                    <input type="text" name="race" placeholder="Race"/>
                </div>

                <div className="submit flexCenter">
                    <input type="submit" value="Add pet"/>
                </div>
            </form>
        </div>
    )
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<ShowPage/>);