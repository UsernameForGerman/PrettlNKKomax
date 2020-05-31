import classes from "./TaskDetailPage.module.css"
import React from "react";
let TaskDetailPage = (props) => {
    return(
        <div className={classes.TaskDetailPage}>
            <div className={classes.container}>
                <div className={`${classes.card} ${classes.left_card}`}>
                <h1>Komax task {props.task_name}</h1>
                <div className={classes.row}>
                    <div className={`${classes.col} ${classes.btnCol}`}>
                        <button className={classes.btnTool}>
                            Full task
                        </button>
                        <button className={classes.btnTool}>
                            Again
                        </button>
                        <button className={classes.btnTool}>
                            Load task
                        </button>
                    </div>
                    <div className={`${classes.col} ${classes.taskCol}`}>
                        {props.task_komax}
                        {props.task_kappa}
                    </div>
                    <div className={`${classes.col} ${classes.ticketCol}`}>
                        {props.ticket_komax}
                        {props.ticket_kappa}
                    </div>
                </div>
            </div>
                <div className={`${classes.card} ${classes.right_card}`}>
                <div className={classes.harnesses}>
                    <h2>
                        Harnesses used
                    </h2>
                    {props.harnesses}
                </div>
                <div className={classes.komaxes}>
                    <h2>
                        Komaxes used
                    </h2>
                    {props.warning
                        ? <>Warning</>
                        : <></>
                    }
                    {props.komaxes}
                </div>
            </div>
            </div>
        </div>
    )
}

export default TaskDetailPage;