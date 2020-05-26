import React, {useState} from "react";
import classes from "./ModalForm.module.css";
import Select from 'react-select';
import MultiSelect from "react-multi-select-component";
import createKomax from "../../../DAL/models/komax";

let ModalForm = (props) => {
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

    return(
        <div className={classes.ModalForm}>
            <div className={classes.heading}>
                <h2>{props.heading}</h2>
                <button onClick={props.close} className={classes.closeBtn}>X</button>
            </div>
            <div className={classes.inputs}>
                <label>
                    Komax number
                    <input type={"text"} className={classes.input} ref={komaxNumberRef} value={currKomax.number}/>
                </label>
                <label>
                    Cтатус
                    <select className={classes.select} ref={statusRef}>
                        <option value={1} selected={currKomax.status === 1} className={classes.option}>1</option>
                        <option value={0} selected={currKomax.status === 0} className={classes.option}>0</option>
                        <option value={2} selected={currKomax.status === 2} className={classes.option}>2</option>
                    </select>
                </label>
                <label>
                    Маркировка
                    <select className={classes.select} ref={markingRef}>
                        <option value={3} selected={currKomax.marking === 3} className={classes.option}>3</option>
                        <option value={2} selected={currKomax.marking === 2} className={classes.option}>2</option>
                        <option value={1} selected={currKomax.marking === 1} className={classes.option}>1</option>
                    </select>
                </label>
                <label>
                    Спаривание
                    <select className={classes.select} ref={pairingRef}>
                        <option value={1} selected={currKomax.pairing === 1} className={classes.option}>1</option>
                        <option value={0} selected={currKomax.pairing === 0} className={classes.option}>0</option>
                    </select>
                </label>
                <label>
                    Сечение
                    <select className={classes.select} ref={sepairingRef}>
                        <option value={"1 2 3"} selected={currKomax.sepairing === "1 2 3"} className={classes.option}>1 2 3</option>
                        <option value={"4 5 6"} selected={currKomax.sepairing === "4 5 6"} className={classes.option}>4 5 6</option>
                        <option value={"7 8 9"} selected={currKomax.sepairing === "7 8 9"} className={classes.option}>7 8 9</option>
                    </select>
                </label>
                <label>
                    Идентификатор
                    <input type={"text"} className={classes.input} value={currKomax.id} ref={identifierRef}/>
                </label>
            </div>
            <div className={classes.toolbar}>
                <button className={classes.saveBtn} onClick={props.close}>
                    Cохранить
                </button>
            </div>
        </div>
    );
}

export default ModalForm;