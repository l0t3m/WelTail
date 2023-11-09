function ShowPage(props) {
    const [choice, setChoice] = React.useState("days");

    const changeSelection = () => {
        daysField.className = "field hidden";
        weeklyField.className = "field hidden";
        monthsField.className = "field hidden";

        let x = repeatType.selectedOptions[0].value

        if (x == "daily") {
            daysField.className="field shown";
        } else if (x == "weekly") {
            weeklyField.className = "field shown";
        } else if (x == "monthly") {
            monthsField.className = "field shown";
        }
        
    }

    return (
        <div>
            <div className="field">
                <div>Repeat this activity?</div>

                <input type="radio" name="repeat" id="off" value="off" onChange={() => display.className = "hidden"}/>
                <div>Off</div>

                <input type="radio" name="repeat" id="on" value="on" onChange={() => display.className = "shown"}/>
                <div>On</div>
            </div>

            <div id="display" className="hidden">
                <div className="field">
                    <div>Repeat type</div>

                    <select name="repeatType" id="repeatType" onChange={() => setChoice(repeatType.selectedOptions[0].value)}>
                        <option value="days">Daily</option>
                        <option value="weeks">Weekly</option>
                        <option value="months">Monthly</option>
                    </select>
                </div>

                
                <div className="field">
                    <div>Repeat every how many {choice}?</div>
                    <input type="number" name="repeatAmount" min="1" placeholder="Number"/>
                </div>
            </div>
        </div>
    )
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<ShowPage/>);