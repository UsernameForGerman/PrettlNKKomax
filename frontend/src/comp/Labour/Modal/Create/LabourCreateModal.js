import classes from './LabourCreateModal.module.css'
import React, {useState} from "react";
import SaveButton from "../../../common/SaveButton/SaveButton";
import {FormattedMessage} from "react-intl";
let LabourCreateModal = (props) => {
    const [time, setTime] = useState();
    const [action, setAction] = useState();
    let send = () => {
        let labour = {
            action : action,
            time : time
        };
        props.close();
        props.createLabour(labour);
    }
    let handleActionChange = (e) => {
        setAction(e.currentTarget.value);
    }
    let handleTimeChange = (e) => {
        setTime(e.currentTarget.value);
    }
    return (
        <div className={classes.form}>
            <div className={classes.heading}><FormattedMessage id={"create_labour"}/></div>
            <label>
                <FormattedMessage id={"action_label"}/>
                <input type={'text'} className={classes.input} value={action} onChange={handleActionChange}/>
            </label>
            <label>
                <FormattedMessage id={"time_label"}/>
                <input type={'number'} className={classes.input} value={time} onChange={handleTimeChange}/>
            </label>
            <SaveButton value={<FormattedMessage id={'save_button_label'}/>} className={classes.input} click={send}/>
        </div>
    )
}

export default LabourCreateModal;