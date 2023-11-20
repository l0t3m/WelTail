function ShowPage(props) {
    const [activity, setActivity] = React.useState([]);

    React.useEffect(()=>{
        axios.get('/api/getTargetedActivity').then((response)=>{
            setActivity(response.data);
        });
    },[]);

    return (
        <div>
            <div className="field">
                <div className="fieldHead">Repeat this activity?</div>
                <div className="flex" id="inputs">
                    {activity.repeat == 0 ?
                        <>
                            <div><input type="radio" name="repeat" value="off" id="repeatOff" required defaultChecked="true" onChange={() => {display.className = "hidden"; AmountInp.value=1}}/>Off</div> {/* checked */}
                            <div><input type="radio" name="repeat" value="on" id="repeatOn" required onChange={() => display.className = "shown"}/>On</div>
                        </>:
                        <>
                            <div><input type="radio" name="repeat" value="off" id="repeatOff" required onChange={() => {display.className = "hidden"; AmountInp.value=1}}/>Off</div>
                            <div><input type="radio" name="repeat" value="on" id="repeatOn" required defaultChecked="true" onChange={() => display.className = "shown"}/>On</div> {/* checked */}
                        </>
                    }
                </div>                
            </div>
            
            <div id="display" className={activity.repeat == 1 ? "shown":"hidden"}>
                <div className="field">
                    <div className="fieldHead">Repeat type</div>
                    <input type="number" name="repeatAmount" id="AmountInp" placeholder="Number" defaultValue={activity.repeatAmount} required min="1"/>
                    <select name="repeatType" id="repeatType">
                        <option value="hours" id="sHours" selected={activity.repeatType == "hours" && "true"}>Hour/s</option>
                        <option value="days" id="sDays" selected={activity.repeatType == "days" && "true"}>Day/s</option>
                        <option value="weeks" id="sWeeks" selected={activity.repeatType == "weeks" && "true"}>Week/s</option>
                        <option value="months" id="sMonths" selected={activity.repeatType == "months" && "true"}>Month/s</option>
                    </select>
                </div>
            </div>
        </div>
    )
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<ShowPage/>);