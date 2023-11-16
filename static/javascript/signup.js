function arrToLowercase(arr) {
    let newArr = []
    arr.map((item) => newArr.push(item.toLowerCase()))
    return newArr
}


function ShowPage(props) {
    const [usernames, setUsernames] = React.useState([]);
    const [usernameState, setUsernameState] = React.useState(false);
    const [passwordState, setpasswordState] = React.useState(false);
    const [submitState, setSubmitState] = React.useState(false);
    const [message, setMessage] = React.useState("")

    React.useEffect(()=>{
        axios.get('/api/allUsernames').then((response)=>{
            setUsernames(response.data);
        });
    },[]);

    const checkUsername = () => {
        setSubmitState(false)
        setUsernameState(false)

        if (myUsername.value.length < 3) {
            setMessage("Username must contain at least 3 characters.")
        } else {
            if (arrToLowercase(usernames).includes(myUsername.value.toLowerCase()) == true) {
                setUsernameState(false)
                setMessage("Username already been taken.")
            } else {
                setMessage("")
                setUsernameState(true)
                if (passwordState == true) {
                    setSubmitState(true)
                    return
                } else {
                    checkPassword()
                }
            }
        }
    }

    const checkPassword = () => {
        setSubmitState(false)
        setpasswordState(false)

        if (myPassword.value.length < 4) {
            setpasswordState(false)
            setMessage("Password must contain at least 4 characters.")
        } else {
            setMessage("")
            setpasswordState(true)
            if (usernameState == true) {
                setSubmitState(true)
                return
            } else {
                checkUsername()
            }
        }
    }

    return (
        <div className="inputsContainer">
            <form action="/signup" method="post">
                <div><input type="text" name="fullname" placeholder="Full Name" id="myname"/></div>
                <div><input type="text" name="username" placeholder="Username" id="myUsername" onInput={() => checkUsername()}/></div>
                <div><input type="password" name="password" placeholder="Password" id="myPassword" onInput={() => checkPassword()}/></div>

                <div>{submitState == false ? <input type="submit" value="Sign Up" disabled/> : <input type="submit" value="Sign Up"/>}</div>

                <div id="display" className="message">{message}</div>
            </form>
        </div>
    )
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<ShowPage/>);