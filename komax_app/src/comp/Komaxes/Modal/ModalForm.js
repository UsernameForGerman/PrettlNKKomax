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

    return(
        <div className={classes.ModalForm}>
            <div className={classes.heading}>
                <h2>{props.heading}</h2>
                <button onClick={props.close} className={classes.closeBtn}>X</button>
            </div>
            <div className={classes.inputs}>
                <label>
                    Komax number
                    <input type={"text"} className={classes.input} value={currKomax.number}/>
                </label>
                <label>
                    Cтатус
                    <select>
                        <option value={1} selected={currKomax.status === 1}>1</option>
                        <option value={0} selected={currKomax.status === 0}>0</option>
                        <option value={2} selected={currKomax.status === 2}>2</option>
                    </select>
                </label>
                <label>
                    Маркировка
                    <select value={currKomax.marking}>
                        <option value={3} selected={currKomax.marking === 3}>3</option>
                        <option value={2} selected={currKomax.marking === 2}>2</option>
                        <option value={1} selected={currKomax.marking === 1}>1</option>
                    </select>
                </label>
                <label>
                    Спаривание
                    <select>
                        <option value={1} selected={currKomax.pairing === 1}>1</option>
                        <option value={0} selected={currKomax.pairing === 0}>0</option>
                    </select>
                </label>
                <label>
                    Сечение
                    <select>
                        <option value={"1 2 3"} selected={currKomax.sepairing === "1 2 3"}>1 2 3</option>
                        <option value={"4 5 6"} selected={currKomax.sepairing === "4 5 6"}>4 5 6</option>
                        <option value={"7 8 9"} selected={currKomax.sepairing === "7 8 9"}>7 8 9</option>
                    </select>
                </label>
                <label>
                    Идентификатор
                    <input type={"text"} className={classes.input} value={currKomax.id}/>
                </label>
            </div>
            <div className={classes.toolbar}>
                <button className={classes.saveBtn} onClick={props.close}>
                    Cохранить
                </button>
            </div>
        </div>
    )
}

export default ModalForm;