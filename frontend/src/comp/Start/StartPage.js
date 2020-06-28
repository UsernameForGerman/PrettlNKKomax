import classes from "./StartPage.module.css"
import React from "react";
import RecentTaskContainer from "./RecentTask/RecentTaskContainer";
let StartPage = (props) => {
    return(
        <div className={classes.StartPage}>
            <h1>Личный кабинет</h1>
            <div className={classes.container}>
                <div className={classes.info}>
                    <div className={classes.header}>
                        <img src={props.ava} alt={"Avatar"} className={classes.ava}/>
                        <div className={classes.username}>{props.username}</div>
                    </div>
                    <div className={classes.content}>
                        <div className={classes.role}>
                            {props.role}
                        </div>
                        <button className={classes.editBtn}>
                            Edit
                        </button>
                    </div>
                </div>
                <div className={classes.recentTasks}>
                    <RecentTaskContainer/>
                </div>
            </div>
        </div>
    )
}

export default StartPage;