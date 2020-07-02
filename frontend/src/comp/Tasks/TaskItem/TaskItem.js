import classes from "./TaskItem.module.css";
import React from "react";
import {NavLink} from "react-router-dom";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {FormattedMessage} from "react-intl";
import task_api from "../../../DAL/task/task_api";
let TaskItem = (props) => {
    return(
        <div className={classes.TaskWrapper}>
            <div className={classes.TaskItem}>
                <div className={classes.heading}>
                    {props.task_name}
                </div>
                <div className={classes.statusBar}>
                    {
                        props.status === 1 && props.role.toLowerCase() === "master"
                            ? <button className={classes.sendTaskBtn} onClick={() => {
                                task_api.sendTask({name : props.task_name}).then(() => {
                                    alert("Задание успешно отправлено");
                                }).catch(() => {
                                    alert("Ошибка отправки");
                                })
                            }}>
                                <FontAwesomeIcon icon={['fas', 'envelope']}/>
                              </button>
                            : props.status === 2
                                ? <button disabled className={classes.taskOrderedBtn}>
                                    <FormattedMessage id={"tasks.ordered_label"}/>
                                  </button>
                                : <>
                                    <button disabled className={classes.taskLoadedBtn}>
                                        <FormattedMessage id={"tasks.loaded_label"}/>
                                    </button>
                                    <button className={classes.deleteTaskBtn}>
                                        <FontAwesomeIcon icon={['fas', 'trash-alt']}/>
                                    </button>
                                  </>
                    }
                    <NavLink to={"/task/" + props.task_name}>
                        <button className={classes.moreBtn}>
                            <FontAwesomeIcon icon={['fas', 'ellipsis-h']}/>
                        </button>
                    </NavLink>
                </div>
            </div>
        </div>
    )
}

export default TaskItem;