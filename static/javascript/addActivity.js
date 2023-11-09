function ShowPage(props) {
    const [choice, setChoice] = React.useState("days");

    return (
        <div>
            <div className="field flex">
                <div>Repeat this activity?</div>

                <input type="radio" name="repeat" id="off" value="off" onChange={() => display.className = "hidden"}/>
                <div>Off</div>

                <input type="radio" name="repeat" id="on" value="on" onChange={() => display.className = "shown"}/>
                <div>On</div>
            </div>

            <div id="display" className="hidden">
                <div className="field">
                    <div>Repeat type</div>

                    <input type="number" name="repeatAmount" min="1" placeholder="Number"/>

                    <select name="repeatType" id="repeatType" onChange={() => setChoice(repeatType.selectedOptions[0].value)}>
                        <option value="hours">Hour/s</option>
                        <option value="days">Day/s</option>
                        <option value="weeks">Week/s</option>
                        <option value="months">Month/s</option>
                    </select>
                </div>
                
            </div>
        </div>
    )
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<ShowPage/>);