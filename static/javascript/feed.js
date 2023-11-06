function ShowPage(props) {
    const [myUser, setMyUser] = React.useState("");
    const [activities, setActivities] = React.useState([]);
    const [message, setMessage] = React.useState("");

    React.useEffect(()=>{
        axios.get('/api/myUser').then((response)=>{
            setMyUser(response.data);
        });

        axios.get('/api/greetingMessage').then((response)=>{
            setMessage(response.data)
        })

        // Add in interval!
        axios.get('/api/myUpcomingActivities').then((response)=>{
            setActivities(response.data);
        });
    },[]);


    return (
        <div className="contentContainer">

            <div className="side">
                <div className="container">

                    <div>{message}, {myUser.username} </div>

                    <hr/>

                    {/* Insert pet selection here through dropdown */}
                    <div>This is the side menu / pet selection.</div>
                    
                    <hr/>

                    {/* Insert user's stats here */}
                    <div className="statsHeader">Stats:</div>
                    <div>user_id - {myUser.user_id} </div>
                    <div>Total activities - {activities.length} </div>
                </div>
            </div>

            <div className="activities">
                {activities.map((activity) => 
                    <div className="container activityContainer">
                        <div className="activity padding">
                            <div className="row">
                                <div className="cell">{activity.name}</div>
                            </div>

                            <div className="row secondRow">
                                <div className="cell">{activity.pet_name}</div>
                                <div className="cell">{activity.type}</div>
                                <div className="cell">{activity.hour}:{activity.minute}, {activity.repeat} ({activity.repeatInterval})</div>
                            </div>
                        </div>

                        <div className="action">
                            <a href={`/activity/done/${activity.user_id}/${activity.activity_id}`}>Done</a>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}



const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<ShowPage/>);