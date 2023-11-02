function ShowPage(props) {
    const [user_id, setUser_id] = React.useState("");
    const [activities, setActivities] = React.useState([]);

    React.useEffect(()=>{
        axios.get('/api/myUserId').then((response)=>{
            setUser_id(response.data);
        });

        // Add in interval!
        axios.get('/api/myUpcomingActivities').then((response)=>{
            setActivities(response.data);
        });
    },[]);


    return (
        <div className="rootContainer">

            <div className="container stats">
                <div>user_id - {user_id} </div>
                <div>Total activities - {activities.length} </div>
            </div>

            {activities.map((activity) => 
                <div className="container activityContainer">
                    <div className="row">
                        <div className="cell">Activity name</div>
                        <div className="cell">{activity.name}</div>
                    </div>

                    <div className="row">
                        <div className="cell">Activity type</div>
                        <div className="cell">{activity.type}</div>
                    </div>

                    <div className="row">
                        <div className="cell">Activity repeat</div>
                        <div className="cell">{activity.repeat}</div>
                    </div>

                    <div className="row">
                        <div className="cell">Activity time</div>
                        <div className="cell">{activity.time}</div>
                    </div>

                    <div className="row">
                        <div className="cell">
                            <a href={`/activity/done/${activity.user_id}/${activity.activity_id}`}>Mark as done</a>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}



const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<ShowPage/>);