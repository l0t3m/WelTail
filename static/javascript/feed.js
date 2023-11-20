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
            axios.get('/api/myPets').then((response)=>{
                setMyPets(response.data);
            });
            axios.get('/api/greetingMessage').then((response)=>{
                setMessage(response.data);
            });
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
        let rate = rateSelect.selectedOptions[0].value;
        let pets = [];
        for (let i = 0; i < checkbox.length; i++) {
            if (checkbox[i].checked == true) {
                pets.push(checkbox[i].value);
            }
        }
        if (pets.length == 0) {
            if (rate == 0) {
                activities.map((activity) => newActs.push(activity));
            } else {
                todayActivities.map((activity) => newActs.push(activity));
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
        setActFiltered(newActs);
    }

    return (
        <div className="contentContainer">
            <div className="side">
                <div className="container sideContainer">
                    <div>{message}, {myUser.fullname} </div>
                    <hr/>
                    <div className={myPets.length == 0 ? "hidden" : null}>
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
                    </div>
                    
                    <div className="sideTable">
                        <div className="sideRow">
                            <div>{myPets.length}</div>
                            <div>{activities.length}</div>
                            <div>{actFiltered.length}</div>
                        </div>
                        <div className="sideRow">
                            <div>Pets</div>
                            <div>Activities</div>
                            <div>Activities Shown</div>
                        </div>
                    </div>

                </div>
            </div>

            <div className="activities">
                {actFiltered.length == 0 ? <FirstActivity activities={activities.length}/> : null}

                {actFiltered.map((activity) => 
                    <div className="container activityContainer">
                        <div className="activity padding">
                            <div className="row">
                                <div className="cell">{activity.name} - {activity.pet_name}</div>
                            </div>
                            <div className="row secondRow">
                                <div className="cell">{activity.type}</div>
                                <div className="cell">{activity.date}</div>
                                <div className="cell">{activity.weekday}, {activity.hour}:{activity.minute}</div>
                                <div className="cell">{activity.repeat}</div>
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

function FirstActivity(props) {
    return (
        <div className="container activityContainer">
            <div className="activity padding">
                <div className="row">
                    {props.activities > 0 ? 
                    <div className="cell">There are no activities assigned for today.</div> : 
                    <div className="cell">There are no activities assigned yet.</div>}
                </div>

                <div className="row secondRow">
                    <div className="cell">To assign new activities, choose one of your pets and add activity.</div>
                </div>
            </div>

            <div className="separator"></div>

            <div className="action">
                <a href={`/profile`} className="done">View pets</a>
            </div>
        </div>)
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<ShowPage/>);