import classes from "./TaskItem.module.css";
import React from "react";
import {NavLink} from "react-router-dom";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {FormattedMessage} from "react-intl";
import task_api from "../../../DAL/task/task_api";
import BASE_URL from "../../../DAL/getBaseUrl";
import RemoveBtn from "./RemoveBtn/RemoveBtn";
let TaskItem = (props) => {
    let loadTask = () => {
        task_api.loadTask(props)
            .then(resp => {
                alert("Заявка успешно отправлена")
            })
            .catch(err => {
                alert("Ошибка при отправке")
            })
    }
    return(
        <div className={classes.TaskWrapper}>
            <div className={classes.TaskItem}>
                <div className={classes.heading}>
                    {props.task_name}
                    <div className={classes.status}>
                        <FormattedMessage id={"status"}/> : {props.status === 1
                            ? <FormattedMessage id={"created"}/>
                            : props.status === 2
                                ? <FormattedMessage id={"tasks.ordered_label"}/>
                                : props.status === 3
                                    ? <FormattedMessage id={"tasks.loaded_label"}/>
                                    : <FormattedMessage id={"completed"}/>
                        }
                    </div>
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
                                ? <button className={classes.taskLoadedBtn} onClick={loadTask}>
                                        <FontAwesomeIcon icon={['fas', 'arrow-up']}/>
                                  </button>
                                : <></>
                    }
                    <RemoveBtn {...props}/>
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