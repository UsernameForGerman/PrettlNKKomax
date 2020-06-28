import classes from "../LabourPage.module.css";
import React from "react";

let LabourItem = (props) => {
    return(
        <div className={classes.data_row} onClick={props.select}>
            <div className={classes.data}>
                {props.action}
            </div>
            <div className={classes.data}>
                {props.time}
            </div>
        </div>
    )
}

export default LabourItem;