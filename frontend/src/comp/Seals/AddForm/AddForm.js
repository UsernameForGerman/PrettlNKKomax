import classes from "./AddForm.module.css"
import React, {useState} from "react";
import SuccessButton from "../../common/SuccessButton/SuccessButton";
import {FormattedMessage} from "react-intl";
let AddForm = (props) => {
    const [selectedOption, setSelectedOption] = useState(true);

    let inputRef = React.createRef();
    let selectRef = React.createRef();

    let handleChange = (e) => {
        let value = e.currentTarget.value;
        setSelectedOption(value);
    }

    let create = () => {
        props.close();
        let data = {
            seal_name : inputRef.current.value,
            seal_available : selectedOption
        }
        props.createSeal(data);
    }

    return (
        <div className={classes.form}>
            <div className={classes.heading}>
                <FormattedMessage id={"create_new_seal"}/>
            </div>
            <label className={classes.label}>
                <div className={classes.input_label}><FormattedMessage id={"seal_name_label"}/></div>
                <input type={"text"} className={classes.input} ref={inputRef}/>
            </label>
            <label className={classes.label}>
                <div className={classes.input_label}><FormattedMessage id={"terminal.material_avaliable_label"}/></div>
                <select className={classes.select} ref={selectRef} value={selectedOption} onChange={handleChange}>
                    <option value={true} className={classes.option}>+</option>
                    <option value={false} className={classes.option}>-</option>
                </select>
            </label>
            <SuccessButton value={<FormattedMessage id={"add_button_text"}/>} click={create} class={classes.succBtn}/>
        </div>
    )
}

export default AddForm;