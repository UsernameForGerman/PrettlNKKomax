import classes from "./TaskDetailPage.module.css"
import React from "react";
import BASE_URL from "../../../DAL/getBaseUrl";
import {Link, NavLink} from "react-router-dom";
import task_api from "../../../DAL/task/task_api";
let TaskDetailPage = (props) => {
    let handleClick = () => {
        task_api.loadTask(props)
            .then(resp => {
                alert("Заявка успешно отправлена")
            })
            .catch(err => {
                alert("Ошибка при отправке")
            })
    }
    return(
        <div className={classes.TaskDetailPage}>
            <div className={classes.container}>
                <div className={`${classes.card} ${classes.left_card}`}>
                <h1>Komax task {props.name}</h1>
                <div className={classes.row}>
                    <div className={`${classes.col} ${classes.btnCol}`}>
                        <a href={BASE_URL + "tasks/" + props.name + "/get_task/"} target={"_blank"}>
                            <button className={classes.btnTool}>
                                Full task
                            </button>
                        </a>
                        <NavLink to={"/task_create/"}>
                            <button className={classes.btnTool}>
                                Again
                            </button>
                        </NavLink>
                        {props.role.toLowerCase() === "operator"
                            ?   <button className={classes.btnTool} onClick={handleClick}>
                                    Load task
                                </button>
                            :   <></>
                        }
                    </div>
                    <div className={`${classes.col} ${classes.taskCol}`}>
                        {props.task_komax}
                    </div>
                    <div className={`${classes.col} ${classes.ticketCol}`}>
                        {props.ticket_komax}
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