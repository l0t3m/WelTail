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
            setMyPets(response.data)
        });

        // Add in interval!
        axios.get('/api/greetingMessage').then((response)=>{
            setMessage(response.data)
        });

        // Add in interval!
        axios.get('/api/myUpcomingActivities').then((response)=>{
            setActivities(response.data);
            setActivitiesFiltered(response.data)
        });
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
            activities.map((activity) => newAct.push(activity));
        }

        if (checkedArr.includes("0")) {
            for (let i = 0; i < checkBoxInput.length; i++) {
                if (checkBoxInput[i].checked == true) {
                    checkBoxInput[i].checked = false;
                }
            }
            checkBoxInput[0].checked = true;

            activities.map((activity) => newAct.push(activity));
        } else {
            activities.map((activity) => checkedArr.includes(String(activity.pet_id)) ? newAct.push(activity) : null);
        }

        setActivitiesFiltered(newAct);
        return;
    }


    return (
        <div className="contentContainer">

            <div className="side">
                <div className="container sideContainer">

                    <div>{message}, {myUser.username} </div>

                    <hr/>

                    <div>
                        <div>Choose a pet to view:</div>

                        <div className="petCheckbox">
                            <div>
                                <input type="checkbox" id="checkBoxInput" value={0} onClick={() => updateFilter()}/>
                                <span class="checkmark"></span>
                            </div>
                            <div>All pets</div>
                        </div>

                        {myPets.map((pet) =>
                            <div className="petCheckbox">
                                <div>
                                    <input type="checkbox" id="checkBoxInput" value={pet.pet_id} onClick={() => updateFilter()}/>
                                    <span class="checkmark"></span>
                                </div>
                                <div>{pet.name}</div>
                            </div>
                        )}
                    </div>

                    <hr/>

                    <div className="statsHeader">Stats:</div>
                    <div>user_id - {myUser.user_id} </div>
                    <div>total pets - {myPets.length}</div>
                    <div>Total activities - {activities.length} </div>
                    <div>Total activities shown - {activitiesFiltered.length} </div>
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