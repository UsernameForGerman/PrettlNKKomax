import React from "react";
import SaveButton from "../../../common/SaveButton/SaveButton";
import classes from "./TCPModal.module.css";
import {FormattedMessage} from "react-intl";

let TaskCreateModalForm = (props) => {
    return(
        <div className={classes.container}>
            <div className={classes.lists}>
                {props.terminal_list}
                {props.seal_list}
            </div>
            <div className={classes.btns}>
                <button onClick={props.close} className={classes.closeBtn}>
                    <FormattedMessage id={"close_label"}/>
                </button>
            </div>
        </div>
    )
}

export default TaskCreateModalForm;