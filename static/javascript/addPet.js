function ShowPage(props) {
    const [myUser, setMyUser] = React.useState("");

    React.useEffect(()=>{
        axios.get('/api/myUser').then((response)=>{
            setMyUser(response.data);
        });

    },[]);


    return (
        <div className="container rootContainer">

            <div className="header">Add a pet</div>

            <form action={`/pet/add/${myUser.user_id}`} method="post">

                <div className="field flex">
                    <input type="radio" name="gender" value="dog"/>
                    <div>Dog</div>

                    <input type="radio" name="gender" value="cat"/>
                    <div>Cat</div>
                </div>

                <div className="field">
                    <input type="text" name="name" placeholder="Name"/>
                </div>

                <div className="field flex">
                    <input type="radio" name="gender" value="male"/>
                    <div>Male</div>

                    <input type="radio" name="gender" value="female"/>
                    <div>Female</div>
                </div>

                <div className="field">
                    <input type="date" name="birthDate" placeholder="Birth Date"/>
                </div>

                <div className="field">
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