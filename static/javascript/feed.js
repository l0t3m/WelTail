function ShowPage(props) {
    const [myUser, setMyUser] = React.useState("");
    const [myPets, setMyPets] = React.useState([]);

    const [activities, setActivities] = React.useState([]);
    const [todayActivities, setTodayActivities] = React.useState([]);
    const [message, setMessage] = React.useState("");
    const [actFiltered, setActFiltered] = React.useState([]);


    React.useEffect(()=>{
        axios.get('/api/myUser').then((response)=>{
            setMyUser(response.data);
        });

        axios.get('/api/myPets').then((response)=>{
            setMyPets(response.data);
        });

        axios.get('/api/greetingMessage').then((response)=>{
            setMessage(response.data);
        });

        axios.get('/api/myActivities').then((response)=>{
            setActivities(response.data);
            setActFiltered(response.data);
        });

        axios.get('/api/myUpcomingActivities').then((response)=>{
            setTodayActivities(response.data);
        });

        setInterval(() => {
            axios.get('/api/myActivities').then((response)=>{
                setActivities(response.data);
            });
            axios.get('/api/myUpcomingActivities').then((response)=>{
                setTodayActivities(response.data);
            });
        }, 30000);
    },[]);

    const updateActivities = () => {
        let newActs = [];
        let rate = rateSelect.selectedOptions[0].value
        let pets = [];
        for (let i = 0; i < checkbox.length; i++) {
            if (checkbox[i].checked == true) {
                pets.push(checkbox[i].value)
            }
        }

        if (pets.length == 0) {
            if (rate == 0) {
                activities.map((activity) => newActs.push(activity))
            } else {
                todayActivities.map((activity) => newActs.push(activity))
            }
        } else {
            if (rate == 0) {
                for (let act of activities) {
                    pets.includes(String(act["pet_id"])) ? newActs.push(act) : null;
                }
            } else {
                for (let act of todayActivities) {
                    pets.includes(String(act["pet_id"])) ? newActs.push(act) : null;
                }
            }
        }
        setActFiltered(newActs)
    }

    return (
        <div className="contentContainer">
            <div className="side">
                <div className="container sideContainer">

                    <div>{message}, {myUser.username} </div>

                    <hr/>

                    <div className="sideHeader">Choose a specific pet/s to view:</div>
                    {myPets.map((pet) =>
                        <div className="petCheckbox">
                            <div>
                                <input type="checkbox" id="checkbox" value={pet.pet_id} onClick={() => updateActivities()}/>
                            </div>
                            <div>{pet.name}</div>
                        </div>
                    )}

                    <hr/>

                    <div className="sideHeader">Select a time range to view:</div>
                    <select name="rateSelect" id="rateSelect" onChange={() => updateActivities()}>
                        <option value={0} selected>All</option>
                        <option value={1}>Today</option>
                    </select>

                    <hr/>

                    <div className="sideHeader">Stats:</div>
                    <div>user_id - {myUser.user_id} </div>
                    <div>total pets - {myPets.length}</div>
                    <div>total activities - {activities.length}</div>
                </div>
            </div>

            <div className="activities">
                {actFiltered.map((activity) => 
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

                        <div className="separator"></div>

                        <div className="action">
                            <a href={`/activity/done/${activity.user_id}/${activity.activity_id}`} className="done">Done</a>
                        </div>

                        <div className="action">
                            <a href={`/petprofile/${activity.user_id}/${activity.pet_id}#${activity.activity_id}`} className="view">View</a>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<ShowPage/>);