import React, {useState} from "react";
import classes from "./ModalForm.module.css";
import createKomax from "../../../DAL/models/komax";
import SaveButton from "../../common/SaveButton/SaveButton";
import {FormattedMessage} from 'react-intl';
import { Multiselect } from 'multiselect-react-dropdown';

let ModalForm = (props) => {
    let [multiselectOptions, setMultiselectOptions] = useState(props.selected ? (props.selected.sepairing ? props.selected.sepairing.trim().split(' ').filter(elem => elem.length > 0) : []) : []);

    let currKomax = props.selected;
    if (!currKomax){
        currKomax = createKomax({});
    }

    let komaxNumberRef = React.createRef();
    let statusRef = React.createRef();
    let markingRef = React.createRef();
    let pairingRef = React.createRef();

    let collectData = (e) => {
        props.close();
        let multiArr = multiselectOptions;
        if (multiArr.length === 0){
            multiArr = currKomax.sepairing.split(" ");
        }
        let data = {
            number : komaxNumberRef.current.value,
            group_of_square : multiArr.reduce((prev, elem) => {
                return prev + " " + elem
            }).trim(),
            pairing : pairingRef.current.value,
            marking : markingRef.current.value,
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

    let handleChoose = (e) => {
        let arr = [];
        e.forEach(elem => {
            arr.push(elem["id"]);
        });
        setMultiselectOptions(arr);
    }

    let options = ['0.5 - 1.0', '1.5 - 2.5', '4.0 - 6.0'].map((elem, index) => {
        return (
            {name : elem, id : index + 1}
        )
    });

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
                <label>
                    <FormattedMessage id={"komax.marking_label"}/>
                    <select className={classes.select} ref={markingRef}>
                        <option value={1} selected={currKomax.marking === 1} className={classes.option}>Black</option>
                        <option value={2} selected={currKomax.marking === 2} className={classes.option}>White</option>
                        <option value={3} selected={currKomax.marking === 3} className={classes.option}>Both</option>
                    </select>
                </label>
                <label>
                    <FormattedMessage id={"komax.pairing_label"}/>
                    <select className={classes.select} ref={pairingRef}>
                        <option value={1} selected={currKomax.pairing === 1} className={classes.option}>+</option>
                        <option value={0} selected={currKomax.pairing === 0} className={classes.option}>-</option>
                    </select>
                </label>
                <label>
                    <FormattedMessage id={"komax.group_of_square_label"}/>
                    <Multiselect
                        options={options} // Options to display in the dropdown
                        onSelect={handleChoose} // Function will trigger on select event
                        onRemove={handleChoose} // Function will trigger on remove event
                        selectedValues={multiselectOptions.map(elem => {
                            return options[new Number(elem) - 1];
                        })}
                        displayValue="name" // Property name to display in the dropdown options
                    />
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