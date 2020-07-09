import classes from './LabourEditModal.module.css'
import React, {useState} from "react";
import SaveButton from "../../../common/SaveButton/SaveButton";
import {FormattedMessage} from "react-intl";
let LabourEditModal = (props) => {
    const [time, setTime] = useState(props.selectedLabour.time);
    let send = () => {
        let labour = {...props.selectedLabour};
        labour.time = time;
        props.close();
        props.updateLabour(labour);
    }
    let handleChange = (e) => {
        setTime(e.currentTarget.value);
    }
    return(
        <div className={classes.form}>
            <div className={classes.heading}><FormattedMessage id={"edit_labour"}/></div>
            <label>
                <FormattedMessage id={"action_label"}/>
                <input type={'text'} className={classes.input} disabled value={props.selectedLabour.action}/>
            </label>
            <label>
                <FormattedMessage id={"time_label"}/>
                <input type={'number'} className={classes.input} value={time} onChange={handleChange}/>
            </label>
            <SaveButton value={<FormattedMessage id={'save_button_label'}/>} click={send}/>
        </div>
    )
}

export default LabourEditModal;