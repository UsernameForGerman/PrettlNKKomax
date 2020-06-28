import classes from './LabourCreateModal.module.css'
import React, {useState} from "react";
import SaveButton from "../../../common/SaveButton/SaveButton";
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
            <div className={classes.heading}>Create labour</div>
            <label>
                Labour action
                <input type={'text'} className={classes.input} value={action} onChange={handleActionChange}/>
            </label>
            <label>
                Labour time
                <input type={'number'} className={classes.input} value={time} onChange={handleTimeChange}/>
            </label>
            <SaveButton value={"Save"} className={classes.input} click={send}/>
        </div>
    )
}

export default LabourCreateModal;