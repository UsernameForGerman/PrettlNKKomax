import React from "react";
import classes from "./RecentTask.module.css"

let RecentTask = (props) => {
    return(
        <div className={classes.recentTask}>
            <div className={classes.heading}>{props.number}</div>
            <div className={classes.lists}>
                <div className={classes.ticket_list}>
                    {props.tickets}
                </div>
                <div className={classes.harness_list}>
                    {props.harnesses}
                </div>
            </div>
        </div>
    )
}

export default RecentTask;