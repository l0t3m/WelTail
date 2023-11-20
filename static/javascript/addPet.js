function ShowPage(props) {
    const [myUser, setMyUser] = React.useState("");

    React.useEffect(()=>{
        axios.get('/api/myUser').then((response)=>{
            setMyUser(response.data);
        });
    },[]);

    return (
        <div className="container rootContainer">
            <div className="header pageHead">Add a new pet</div>
            <form action={`/pet/add/${myUser.user_id}`} method="post">
                <div className="field">
                    <div className="fieldHead">Type of pet</div>
                    <div className="flex species">
                        <div><input type="radio" name="species" value="dog" required/>Dog</div>
                        <div><input type="radio" name="species" value="cat" required/>Cat</div>
                    </div>
                </div>

                <div className="field">
                    <div className="fieldHead">Name</div>
                    <input type="text" name="name" placeholder="Name" required minlength="3"/>
                </div>

                <div className="field">
                    <div className="fieldHead">Gender</div>
                    <div className="flex gender">
                        <div><input type="radio" name="gender" value="male" required/>Male</div>
                        <div><input type="radio" name="gender" value="female" required/>Female</div>
                    </div>
                </div>

                <div className="field">
                    <div className="fieldHead">Date of birth</div>
                    <input type="date" name="birthDate" placeholder="Birth Date" required max={new Date().toISOString().split("T")[0]}/>
                </div>

                <div className="field">
                    <div className="fieldHead">Race</div>
                    <input type="text" name="race" placeholder="Race" required minlength="3"/>
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