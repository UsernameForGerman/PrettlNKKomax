import classes from "./TaskItem.module.css";
import React from "react";
import {NavLink} from "react-router-dom";
let TaskItem = (props) => {
    return(
        <div className={classes.TaskWrapper}>
            <div className={classes.TaskItem}>
                <div className={classes.heading}>
                    {props.number}
                </div>
                <div className={classes.statusBar}>
                    {
                        props.status === 1
                            ? <button className={classes.sendTaskBtn}>
                                Send task
                              </button>
                            : props.status === 2
                                ? <button disabled className={classes.taskOrderedBtn}>
                                    Task ordered
                                  </button>
                                : <>
                                    <button disabled className={classes.taskLoadedBtn}>
                                        Task loaded
                                    </button>
                                    <button className={classes.deleteTaskBtn}>
                                        Delete task
                                    </button>
                                  </>
                    }
                    <NavLink to={props.link}>
                        <button className={classes.moreBtn}>
                            More
                        </button>
                    </NavLink>
                </div>
            </div>
        </div>
    )
}

export default TaskItem;