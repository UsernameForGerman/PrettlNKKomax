import RecentTask from "./RecentTask";
import React from "react";
import classes from "./RecentTask.module.css"

let RecentTaskContainer = (props) => {
    let ticket_komax = props.komaxes.map(elem => {
        return(
            <a href={BASE_URL + "tasks/" + props.name +"/get_ticket_komax/" + elem.komax +"/"} target={"blank"}>
                <button className={classes.greenBtn}>
                    Ticket {elem.komax}
                </button>
            </a>
        )
    });

    let harnesses_btns = props.harnesses.map(elem => {
        return(
            <div className={classes.harness}>
                <div className={classes.heading}>
                    Harness {elem.harness}
                </div>
                <div className={classes.status}>
                    {props.percent} % completed
                </div>
                <a href={BASE_URL + "tasks/" + props.name +"/harnesses/" + elem.harness +"/download/"} target={"blank"}>
                    <button className={classes.greenBtn}>
                        Download
                    </button>
                </a>
            </div>
        )
    });

    return (
        <RecentTask {...props} tickets={ticket_komax} harnesses={harnesses_btns}/>
    )
}

export default RecentTaskContainer;