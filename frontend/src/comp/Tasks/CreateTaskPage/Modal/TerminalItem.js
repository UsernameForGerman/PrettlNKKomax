import React, {useState} from "react";
import classes from "./TCPModal.module.css";

let TerminalItem = (terminal) => {
    let [available, setAvailable] = useState(terminal.terminal_available);
    let change = (e) => {
        setAvailable(e.currentTarget.value);
        let copy = {...terminal};
        copy.terminal_available = e.currentTarget.value;
        terminal.updateTerminal(copy);
    }
    return (
        <div className={classes.row}>
            <div className={classes.item}>
                {terminal.terminal_name}
            </div>
            <div className={classes.item}>
                <select value={available} onChange={change} className={classes.select}>
                    <option value={true}>+</option>
                    <option value={false}>-</option>
                </select>
            </div>
        </div>
    )
}

export default TerminalItem;