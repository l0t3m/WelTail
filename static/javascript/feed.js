function ShowPage(props) {
    const [myUser, setMyUser] = React.useState("");
    const [myPets, setMyPets] = React.useState([]);

    const [activities, setActivities] = React.useState([]);
    const [message, setMessage] = React.useState("");
    const [activitiesFiltered, setActivitiesFiltered] = React.useState([]);

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

        axios.get('/api/myUpcomingActivities').then((response)=>{
            setActivities(response.data);
            setActivitiesFiltered(response.data);
        });



        setInterval(() => {
            axios.get('/api/myUpcomingActivities').then((response)=>{
                setActivities(response.data);
            });
        }, 10000);
        
    },[]);


    const updateFilter = () => {
        let checkedArr = [];
        let newAct = [];

        for (let i = 0; i < checkBoxInput.length; i++) {
            if (checkBoxInput[i].checked == true) {
                checkedArr.push(checkBoxInput[i].value);
            }
        }

        if (checkedArr.length == 0) {
            activities.map((activity) => newAct.push(activity))
        } else {
            activities.map((activity) => checkedArr.includes(String(activity.pet_id)) ? newAct.push(activity) : null);
        }
        setActivitiesFiltered(newAct);
        return;
    }

    const updateRate = () => {
        let rate = rateSelect.selected
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
                                <input type="checkbox" id="checkBoxInput" value={pet.pet_id} onClick={() => updateFilter()}/>
                            </div>
                            <div>{pet.name}</div>
                        </div>
                    )}

                    <hr/>

                    <div className="sideHeader">Select a specific time to view:</div>

                    <select name="rateSelect" id="rateSelect">
                        <option value="1" selected>Today</option>
                        <option value="2">Tomorrow</option>
                        <option value="0">All</option>
                    </select>

                    <hr/>

                    <div className="sideHeader">Stats:</div>
                    <div>user_id - {myUser.user_id} </div>
                    <div>total pets - {myPets.length}</div>
                    <div>total activities - {activities.length}</div>
                </div>
            </div>

            <div className="activities">
                {activitiesFiltered.map((activity) => 
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