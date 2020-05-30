import classes from "./TasksPage.module.css"
import React from "react";
import SuccessButton from "../common/SuccessButton/SuccessButton";
import {NavLink} from "react-router-dom";
let TaskPage = (props) => {
    return(
        <div className={classes.TaskPage}>
            <div className={classes.heading}>
                <div className={classes.username}>
                    <h1>{props.username}</h1>
                </div>
                <div className={classes.title}>
                    <h1>Страница всех заданий</h1>
                </div>
                <NavLink to={"task_create/"}>
                    <SuccessButton class={classes.addBtn} value={"+"}/>
                </NavLink>
            </div>
            <div className={classes.container}>
                {props.rows}
            </div>
        </div>
    )
}

export default TaskPage;