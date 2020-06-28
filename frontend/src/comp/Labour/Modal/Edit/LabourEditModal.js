import classes from './LabourEditModal.module.css'
import React, {useState} from "react";
import SaveButton from "../../../common/SaveButton/SaveButton";
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
            <div className={classes.heading}>Edit labour</div>
            <label>
                Labour action
                <input type={'text'} disabled value={props.selectedLabour.action}/>
            </label>
            <label>
                Labour time
                <input type={'text'} value={time} onChange={handleChange}/>
            </label>
            <SaveButton value={"Save"} click={send}/>
        </div>
    )
}

export default LabourEditModal;