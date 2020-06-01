import classes from "./IconButton.module.css"
import React from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
let IconButton = (props) => {
    return(
        <button className={`${classes.iconButton} ${props.class}`} onClick={props.click} disabled={props.disable}>
            <FontAwesomeIcon icon={props.icon}/>
        </button>
    );
}

export default IconButton;