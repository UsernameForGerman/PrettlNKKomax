import React, {useState} from "react";
import classes from "./ModalForm.module.css";
import {FormattedMessage} from "react-intl";
import SaveButton from "../../common/SaveButton/SaveButton";

let ModalForm = (props) => {
    let terminalNumberRef = React.createRef();
    let terminalAvalRef = React.createRef();
    let materialAvalRef = React.createRef();

    let collectData = (e) => {
        props.close();
        let data = {
            terminal_name : terminalNumberRef.current.value,
            terminal_avaliable : terminalAvalRef.current.value,
            material_avaliable : materialAvalRef.current.value
        }

        props.send(data);
    };

    let isNumberValid = props.numberErrMsg.length === 0;

    return(
        <div className={classes.ModalForm}>
            <div className={classes.heading}>
                <h2><FormattedMessage id={"terminal.edit_terminal_heading"}/></h2>
                <button onClick={props.close} className={classes.closeBtn}>X</button>
            </div>
            <div className={classes.inputs}>
                <label>
                    <FormattedMessage id={"terminal.terminal_number_label"}/>
                    <input type={"text"} className={`${classes.input} ${!isNumberValid ? classes.invalidInput :""}`} ref={terminalNumberRef} value={props.selected.terminal_name} disabled/>
                </label>
                <label>
                    <FormattedMessage id={"terminal.terminal_avaliable_label"}/>
                    <select className={classes.select} ref={terminalAvalRef}>
                        <option value={"True"} className={classes.option}>True</option>
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
                <SaveButton click={collectData} disable={props.isFetching || !props.isValid} value={<FormattedMessage id={"save_button_label"}/>}>
                    <FormattedMessage id={"save_button_label"}/>
                </SaveButton>
            </div>
        </div>
    );
}

export default ModalForm;