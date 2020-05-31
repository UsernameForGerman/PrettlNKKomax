import classes from "./TaskItem.module.css";
import React from "react";
import {NavLink} from "react-router-dom";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {FormattedMessage} from "react-intl";
let TaskItem = (props) => {
    return(
        <div className={classes.TaskWrapper}>
            <div className={classes.TaskItem}>
                <div className={classes.heading}>
                    {props.task_name}
                </div>
                <div className={classes.statusBar}>
                    {
                        props.status === 1
                            ? <button className={classes.sendTaskBtn}>
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
                    <NavLink to={"/task/" + props.number}>
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