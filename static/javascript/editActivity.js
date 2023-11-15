function ShowPage(props) {
    const [activity, setActivity] = React.useState([])

    React.useEffect(()=>{
        axios.get('/api/getTargetedActivity').then((response)=>{
            setActivity(response.data)
        });
    },[]);

    return (
        <div>
            <div className="field flex">
                <div>Repeat this activity?</div>

                <input type="radio" name="repeat" value="off" id="repeatOff" onChange={() => display.className = "hidden"}/>
                <div>Off</div>
                <input type="radio" name="repeat" value="on" id="repeatOn" onChange={() => display.className = "shown"}/>
                <div>On</div>
            </div>

            <div id="display" className="hidden">
                <div className="field">
                    <div>Repeat type</div>
                    <input type="number" name="repeatAmount" min="1" placeholder={activity.repeatAmount}/>

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