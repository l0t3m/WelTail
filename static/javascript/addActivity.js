function ShowPage(props) {
    return (
        <div>
            <div className="field">
                <div className="fieldHead">Repeat this activity?</div>

                <div className="flex">
                    <div><input type="radio" name="repeat" value="off" onChange={() => display.className = "hidden"}/>Off</div>
                    <div><input type="radio" name="repeat" value="on" onChange={() => display.className = "shown"}/>On</div>
                </div>
            </div>

            <div id="display" className="hidden">
                <div className="field">
                    <div className="fieldHead">Repeat type</div>

                    <input type="number" name="repeatAmount" min="1" placeholder="Number"/>

                    <select name="repeatType" id="repeatType">
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