import React, {useState} from "react";
import classes from "./TCPModal.module.css";

let SealItem = (seal) => {
    let [available, setAvailable] = useState(seal.seal_available);
    let change = (e) => {
        setAvailable(e.currentTarget.value);
        let copy = {...seal};
        copy.seal_available = e.currentTarget.value;
        seal.callback(copy);
    }
    return (
        <div className={classes.row}>
            <div className={classes.item}>
                {seal.seal_name}
            </div>
            <div className={classes.item}>
                <select value={available} onChange={change} className={classes.select}>
                    <option className={classes.option} value={true}>+</option>
                    <option className={classes.option} value={false}>-</option>
                </select>
            </div>
        </div>
    )
}

export default SealItem;