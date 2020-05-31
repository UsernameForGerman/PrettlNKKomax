import React, {useState} from "react";
import classes from "./ModalForm.module.css";
import createKomax from "../../../DAL/models/komax";
import SaveButton from "../../common/SaveButton/SaveButton";
import {FormattedMessage} from 'react-intl';

let ModalForm = (props) => {
    let [multiselectOptions, setMultiselectOptions] = useState([]);

    let currKomax = props.selected;
    if (!currKomax){
        currKomax = createKomax({});
    }

    let komaxNumberRef = React.createRef();
    let statusRef = React.createRef();
    let markingRef = React.createRef();
    let pairingRef = React.createRef();
    let sepairingRef = React.createRef();
    let identifierRef = React.createRef();

    let collectData = (e) => {
        debugger;
        props.close();
        let multiArr = multiselectOptions;
        if (multiArr.length === 0){
            multiArr = currKomax.sepairing.split(" ");
        }
        let data = {
            number : komaxNumberRef.current.value,
            identifier : identifierRef.current.value,
            group_of_square : multiArr.reduce((prev, elem) => {
                return prev + " " + elem
            }).trim(),
            pairing : pairingRef.current.value,
            marking : markingRef.current.value,
            status : statusRef.current.value
        }

        debugger;
        props.send(data);
    };

    let isInEditMode = props.heading === "Изменить существующий аппарат";
    let isNumberValid = props.numberErrMsg.length === 0;
    let isIdValid = props.idErrMsg.length === 0;

    let check = (e) => {
        if (!isInEditMode){
            let number = Number(komaxNumberRef.current.value);
            let id = identifierRef.current.value;
            props.checkValid(number, id);
        }
    }

    let handleMultiSelect = (e) => {
        let arr = [];
        let options = e.target.selectedOptions;
        for (let option in options) {
            let value = options[option].value;
            if (value){
                arr.push(Number(value));
            }
        }
        setMultiselectOptions(arr);
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
                        <option value={0} selected={currKomax.status === 0} className={classes.option}>Works</option>
                        <option value={0} selected={currKomax.status === 0} className={classes.option}>Repair</option>
                        <option value={2} selected={currKomax.status === 2} className={classes.option}>Not working</option>
                    </select>
                </label>
                <label>
                    <FormattedMessage id={"komax.marking_label"}/>
                    <select className={classes.select} ref={markingRef}>
                        <option value={3} selected={currKomax.marking === 3} className={classes.option}>Black</option>
                        <option value={2} selected={currKomax.marking === 2} className={classes.option}>White</option>
                        <option value={1} selected={currKomax.marking === 1} className={classes.option}>Both</option>
                    </select>
                </label>
                <label>
                    <FormattedMessage id={"komax.pairing_label"}/>
                    <select className={classes.select} ref={pairingRef}>
                        <option value={1} selected={currKomax.pairing === 1} className={classes.option}>Yes</option>
                        <option value={0} selected={currKomax.pairing === 0} className={classes.option}>No</option>
                    </select>
                </label>
                <label>
                    <FormattedMessage id={"komax.group_of_square_label"}/>
                    <select className={classes.select} multiple={true} ref={sepairingRef} onChange={handleMultiSelect}>
                        <option value={1} selected={currKomax.sepairing && currKomax.sepairing.indexOf("1") !== -1} className={classes.option}>0.5 - 1.0</option>
                        <option value={2} selected={currKomax.sepairing && currKomax.sepairing.indexOf("2") !== -1} className={classes.option}>1.5 - 2.5</option>
                        <option value={3} selected={currKomax.sepairing && currKomax.sepairing.indexOf("3") !== -1} className={classes.option}>4.0 - 6.0</option>
                    </select>
                </label>
                <label>
                    <FormattedMessage id={"komax.identifier_label"}/>
                    <input type={"text"} className={`${classes.input} ${!isIdValid ? classes.invalidInput :""}`} value={currKomax.id} ref={identifierRef} onChange={check} disabled={isInEditMode}/>
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

export default ModalForm;