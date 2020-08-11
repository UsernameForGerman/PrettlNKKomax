import React, {useState} from "react";
import classes from "./KappaModalForm.module.css";
import createKomax from "../../../DAL/models/komax";
import SaveButton from "../../common/SaveButton/SaveButton";
import {FormattedMessage} from 'react-intl';
import { Multiselect } from 'multiselect-react-dropdown';

let KappaModalForm = (props) => {

    let currKomax = props.selected;
    if (!currKomax){
        currKomax = createKomax({});
    }

    let komaxNumberRef = React.createRef();
    let statusRef = React.createRef();

    let collectData = (e) => {
        props.close();
        let data = {
            number : komaxNumberRef.current.value,
            status : statusRef.current.value
        }

        props.send(data);
    };

    let isInEditMode = props.heading === "Изменить существующий аппарат";
    let isNumberValid = props.numberErrMsg.length === 0;
    let isIdValid = props.idErrMsg.length === 0;

    let check = (e) => {
        if (!isInEditMode){
            let number = Number(komaxNumberRef.current.value);
            props.checkValid(number);
        }
    }

    return(
        <div className={classes.ModalForm}>
            <div className={classes.heading}>
                <h2>{props.heading}</h2>
                <button onClick={props.close} className={classes.closeBtn}>X</button>
            </div>
            <div className={classes.inputs}>
                <label>
                    <FormattedMessage id={"komax.number_label"}/>
                    <input type={"text"} className={`${classes.input} ${!isNumberValid ? classes.invalidInput :""}`} ref={komaxNumberRef} value={currKomax.number} onChange={check} disabled={isInEditMode}/>
                </label>
                {isNumberValid
                    ? <></>
                    : <div className={classes.error}>
                        {props.numberErrMsg}
                      </div>
                }
                <label>
                    <FormattedMessage id={"komax.status_label"}/>
                    <select className={classes.select} ref={statusRef}>
                        <option value={1} selected={currKomax.status === 1} className={classes.option}>Works</option>
                        <option value={2} selected={currKomax.status === 0} className={classes.option}>Repair</option>
                        <option value={3} selected={currKomax.status === 2} className={classes.option}>Not working</option>
                    </select>
                </label>
                {isIdValid
                    ? <></>
                    : <div className={classes.error}>
                        {props.idErrMsg}
                      </div>
                }
            </div>
            <div className={classes.toolbar}>
                <SaveButton click={collectData} disable={props.isFetching || !props.isValid} value={<FormattedMessage id={"save_button_label"}/>}/>
            </div>
        </div>
    );
}

export default KappaModalForm;