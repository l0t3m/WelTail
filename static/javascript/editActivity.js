function ShowPage(props) {
    const [activity, setActivity] = React.useState([])

    React.useEffect(()=>{
        axios.get('/api/getTargetedActivity').then((response)=>{
            setActivity(response.data)
        });
    },[]);

    return (
        <div>
            <div className="field">
                <div className="fieldHead">Repeat this activity?</div>
                <div className="flex">
                    <div><input type="radio" name="repeat" value="off" id="repeatOff" onChange={() => display.className = "hidden"} required/>Off</div>
                    <div><input type="radio" name="repeat" value="on" id="repeatOn" onChange={() => display.className = "shown"} required/>On</div>
                </div>                
            </div>

            <div id="display" className="hidden">
                <div className="field">
                    <div className="fieldHead">Repeat type</div>
                    <input type="number" name="repeatAmount" placeholder={activity.repeatAmount} required min="1"/>
                    <select name="repeatType" id="repeatType">
                        <option value="hours" id="sHours">Hour/s</option>
                        <option value="days" id="sDays">Day/s</option>
                        <option value="weeks" id="sWeeks">Week/s</option>
                        <option value="months" id="sMonths">Month/s</option>
                    </select>
                </div>
            </div>

            <div className="hidden">
                {activity.repeat == 1 ? (repeatOn.checked = true) : null}
                {activity.repeat == 0 ? (repeatOff.checked = true) : null}
                {activity.repeat == 1 ? (display.className = "shown") : null}

                {activity.repeatType == "hours" ? (sHours.selected = true) : null}
                {activity.repeatType == "days" ? (sDays.selected = true) : null}
                {activity.repeatType == "weeks" ? (sWeeks.selected = true) : null}
                {activity.repeatType == "months" ? (sMonths.selected = true) : null}
            </div>
        </div>
    )
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<ShowPage/>);