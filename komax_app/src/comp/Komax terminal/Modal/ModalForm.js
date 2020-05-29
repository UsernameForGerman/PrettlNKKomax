import React, {useState} from "react";
import classes from "./ModalForm.module.css";
import Select from 'react-select';
import MultiSelect from "react-multi-select-component";
import createKomax from "../../../DAL/models/komax";
import createTerminal from "../../../DAL/models/terminal";
import {FormattedMessage} from "react-intl";

let ModalForm = (props) => {
    let terminalNumberRef = React.createRef();
    let terminalAvalRef = React.createRef();
    let materialAvalRef = React.createRef();

    let collectData = (e) => {
        props.close();
        let data = {
            terminal_number : terminalNumberRef.current.value,
            terminal_avaliable : terminalAvalRef.current.value,
            material_avaliable : materialAvalRef.current.value
        }

        props.send(data);
    };

    let isNumberValid = props.numberErrMsg.length === 0;

    let check = (e) => {
        let number = Number(terminalNumberRef.current.value);
        debugger;
        console.log(number);
    }

    return(
        <div className={classes.ModalForm}>
            <div className={classes.heading}>
                <h2><FormattedMessage id={"terminal.create_terminal_heading"}/></h2>
                <button onClick={props.close} className={classes.closeBtn}>X</button>
            </div>
            <div className={classes.inputs}>
                <label>
                    <FormattedMessage id={"terminal.terminal_number_label"}/>
                    <input type={"text"} className={`${classes.input} ${!isNumberValid ? classes.invalidInput :""}`} ref={terminalNumberRef} onChange={check}/>
                    {isNumberValid
                        ? <></>
                        : <div className={classes.error}>
                            {props.numberErrMsg}
                          </div>
                    }
                </label>
                <label>
                    <FormattedMessage id={"terminal.terminal_avaliable_label"}/>
                    <select className={classes.select} ref={terminalAvalRef}>
                        <option value={"True"} selected className={classes.option}>True</option>
                        <option value={"False"} className={classes.option}>False</option>
                    </select>
                </label>
                <label>
                    <FormattedMessage id={"terminal.material_avaliable_label"}/>
                    <select className={classes.select} ref={materialAvalRef}>
                        <option value={"True"} selected className={classes.option}>True</option>
                        <option value={"False"} className={classes.option}>False</option>
                    </select>
                </label>
            </div>
            <div className={classes.toolbar}>
                <button className={classes.saveBtn} onClick={collectData} disabled={props.isFetching || !props.isValid}>
                    <FormattedMessage id={"save_button_label"}/>
                </button>
            </div>
        </div>
    );
}

export default ModalForm;