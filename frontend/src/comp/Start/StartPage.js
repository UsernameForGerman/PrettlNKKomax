import classes from "./StartPage.module.css"
import React from "react";
import SuccessButton from "../common/SuccessButton/SuccessButton";
import {FormattedMessage} from "react-intl";
let StartPage = (props) => {
    return(
        <div className={classes.StartPage}>
            <div className={classes.container}>
                <div className={classes.heading}>
                    <div className={classes.username}>
                        <h1>{props.username}</h1>
                    </div>
                    <SuccessButton class={classes.addBtn} value={"+"}/>
                </div>
                <div className={classes.recentTasks}>
                    {props.tasks}
                </div>
            </div>
        </div>
    )
}

export default StartPage;