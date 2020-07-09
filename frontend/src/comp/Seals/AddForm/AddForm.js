import classes from "./AddForm.module.css"
import React, {useState} from "react";
import SuccessButton from "../../common/SuccessButton/SuccessButton";
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
                Create new seal
            </div>
            <label className={classes.label}>
                <div className={classes.input_label}>Seal name</div>
                <input type={"text"} className={classes.input} ref={inputRef}/>
            </label>
            <label className={classes.label}>
                <div className={classes.input_label}>Seal available</div>
                <select className={classes.select} ref={selectRef} value={selectedOption} onChange={handleChange}>
                    <option value={true} className={classes.option}>+</option>
                    <option value={false} className={classes.option}>-</option>
                </select>
            </label>
            <SuccessButton value={"Create"} click={create} class={classes.succBtn}/>
        </div>
    )
}

export default AddForm;