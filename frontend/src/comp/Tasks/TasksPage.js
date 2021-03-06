import classes from "./TasksPage.module.css"
import React from "react";
import SuccessButton from "../common/SuccessButton/SuccessButton";
import {NavLink} from "react-router-dom";
import {FormattedMessage} from "react-intl";
let TaskPage = (props) => {
    return(
        <div className={classes.TaskPage}>
            <div className={classes.heading}>
                <div className={classes.username}>
                    <div>{props.username}</div>
                </div>
                <div className={classes.title}>
                    <h1><FormattedMessage id={"tasks.all_tasks_page_heading"}/></h1>
                </div>
                {props.role.toString().toLowerCase() !== 'operator'
                    ?   <NavLink to={"task_create/"}>
                            <SuccessButton class={classes.addBtn} value={"+"}/>
                        </NavLink>
                    :   <></>
                }
            </div>
            <div className={classes.container}>
                {props.rows}
            </div>
        </div>
    )
}

export default TaskPage;