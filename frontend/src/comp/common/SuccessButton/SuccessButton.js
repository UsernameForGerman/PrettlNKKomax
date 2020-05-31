import classes from "./SuccessButton.module.css"
import React from "react";
let SuccessButton = (props) => {
    return(
        <button className={`${classes.succBtn} ${props.class}`} onClick={props.click}>
            {props.value}
        </button>
    );
}

export default SuccessButton;