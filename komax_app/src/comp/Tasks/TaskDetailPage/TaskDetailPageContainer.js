import TaskDetailPage from "./TaskDetailPage";
import React from "react";
import {withRouter} from "react-router-dom";
import auth from "../../AuthHOC/authHOC";
import classes from "./TaskDetailPage.module.css"

let TaskDetailPageContainer = (props) => {
    let name = props.match.params.id;
    let items = [
        {
            number : "14-123-22321"
        },
        {
            number : "1123-221-321"
        },
        {
            number : "675-34798-21"
        },
        {
            number : "16678564-765"
        },
    ];

    let harnesses = [
        {
            number : "123123",
            amount : 12
        },
        {
            number : "675436",
            amount : 42
        },
        {
            number : "896342136",
            amount : 223
        },
    ].map(elem => {
        return(
            <h3 className={classes.harness}>
                {elem.number} : {elem.amount}
            </h3>
        )
    });

    let komaxes = [
        {
            number : "123123",
            time : 12312
        },
        {
            number : "231",
            time : 123554
        },
        {
            number : "123",
            time : 967745
        },
    ].map(elem => {
        return(
            <h3 className={classes.komax}>
                {elem.number} - {elem.time}
            </h3>
        )
    });

    let task_komax = items.map(elem => {
        return(
            <button className={classes.greenBtn}>
                Task {elem.number}
            </button>
        )
    });

    let ticket_komax = items.map(elem => {
        return(
            <button className={classes.greenBtn}>
                Ticket {elem.number}
            </button>
        )
    });
    return(
        <TaskDetailPage
            task_name={name}
            task_komax={task_komax}
            task_kappa={task_komax}
            ticket_komax={ticket_komax}
            ticket_kappa={ticket_komax}
            harnesses={harnesses}
            komaxes={komaxes}
        />
    )
}

export default auth(withRouter(TaskDetailPageContainer))