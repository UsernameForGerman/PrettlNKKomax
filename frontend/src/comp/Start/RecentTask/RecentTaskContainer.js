import RecentTask from "./RecentTask";
import React from "react";
import classes from "./RecentTask.module.css"
import task_status from "../../../DAL/task_status/task_status";
const BASE_URL = "http://localhost:8000/"
let RecentTaskContainer = (props) => {
    let komaxes = [
        {komax : 3},
        {komax : 5}
    ]

    let harnesses = [
        {
            harness : "123214-132",
            percent : 50
        },

        {
            harness : "126544-754",
            percent : 30
        },
    ]

    let name = 1234;

    let ticket_komax = komaxes.map(elem => {
        return(
            <a href={BASE_URL + "tasks/" + name +"/get_ticket_komax/" + elem.komax +"/"} target={"blank"}>
                <button className={classes.greenBtn}>
                    Ticket {elem.komax}
                </button>
            </a>
        )
    });

    let harnesses_btns = harnesses.map(elem => {
        return(
            <div className={classes.harness}>
                <div className={classes.harness_heading}>
                    Harness {elem.harness}
                </div>
                <div className={classes.status}>
                    {elem.percent} % completed
                </div>
                <a href={BASE_URL + "tasks/" + name +"/harnesses/" + elem.harness +"/download/"} target={"blank"}>
                    <button className={classes.greenBtn}>
                        Download
                    </button>
                </a>
            </div>
        )
    });

    return (
        <RecentTask {...props} tickets={ticket_komax} harnesses={harnesses_btns} number={name}/>
    )
}

export default RecentTaskContainer;