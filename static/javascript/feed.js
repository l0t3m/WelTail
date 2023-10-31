function ShowPage(props) {
    const [user_id, setUser_id] = React.useState("");
    const [activities, setActivities] = React.useState([]);

    React.useEffect(()=>{
        axios.get('/myUser').then((response)=>{
            setUser_id(response.data);
        });
        axios.get('/myActivities').then((response)=>{
            setActivities(response.data);
        });
    },[]);


    return (
        <div className="container">
            <div>user_id - {user_id} </div>

            {activities.map((activity) => 
                <div className="activityContainer">
                    <div className="row">
                        <div className="cell">userid</div>
                        <div className="cell">{activity.user_id}</div>
                    </div>

                    <div className="row">
                        <div className="cell">petid</div>
                        <div className="cell">{activity.pet_id}</div>
                    </div>

                    <div className="row">
                        <div className="cell">activityid</div>
                        <div className="cell">{activity.activity_id}</div>
                    </div>

                    <div className="row">
                        <div className="cell">Activity name</div>
                        <div className="cell"> {activity.name} </div>
                    </div>

                    <div className="row">
                        <div className="cell">Next Alert</div>
                        <div className="cell"> {activity.nextAlert} </div>
                    </div>

                    <div className="row">
                        <div className="cell">Repeat</div>
                        <div className="cell"> {activity.repeat} </div>
                    </div>

                    <div className="row">
                        <div className="cell">Repeat Interval</div>
                        <div className="cell"> {activity.repeatInterval} </div>
                    </div>
                </div>
            )}

            
            <div>total - {activities.length}</div>

        </div>
    )
}



const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<ShowPage/>);