import classes from "./TaskDetailPage.module.css"
import React from "react";
import BASE_URL from "../../../DAL/getBaseUrl";
import {Link, NavLink} from "react-router-dom";
import task_api from "../../../DAL/task/task_api";
import {FormattedMessage} from "react-intl";
let TaskDetailPage = (props) => {
    let handleClick = () => {
        debugger;
        task_api.loadTask({task_name : props.name})
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
                    <h1><FormattedMessage id={"task_label"}/> {props.name}</h1>
                    <div className={classes.row}>
                        <div className={`${classes.row} ${classes.btnCol}`}>
                            <a href={BASE_URL + "api/v1/" + props.name + "/get_task/"} target={"_blank"}>
                                <button className={classes.btnTool}>
                                    <FormattedMessage id={"full_task_label"}/>
                                </button>
                            </a>
                            <NavLink to={"/task_create/"}>
                                <button className={classes.btnTool}>
                                    <FormattedMessage id={"again"}/>
                                </button>
                            </NavLink>
                            {props.role.toLowerCase() === "operator"
                                ?   <button className={classes.btnTool} onClick={handleClick}>
                                        <FormattedMessage id={"load_task_label"}/>
                                    </button>
                                :   <></>
                            }
                        </div>
                    </div>
                    <div className={classes.row}>
                        <div className={`${classes.col} ${classes.taskCol}`}>
                            {props.task_komax}
                        </div>
                    </div>
                    <div className={classes.row}>
                        <div className={`${classes.col} ${classes.ticketCol}`}>
                            {props.ticket_komax}
                        </div>
                    </div>
                    <div className={classes.col}>
                        <div className={classes.harnesses}>
                            <h2>
                                <FormattedMessage id={"harnesses_used"}/>
                            </h2>
                            {props.harnesses}
                        </div>
                        <div className={classes.komaxes}>
                            <h2>
                                <FormattedMessage id={"komaxes_used"}/>
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
        </div>
    )
}

export default TaskDetailPage;