import classes from "./SaveButton.module.css"
import React from "react";
let SaveButton = (props) => {
    return(
        <button className={`${classes.saveBtn} ${props.class}`} onClick={props.click} disabled={props.disable}>
            {props.value}
        </button>
    );
}

export default SaveButton;