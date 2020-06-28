import classes from "./ChooseModal.module.css";
import React, {useState} from "react";
import SaveButton from "../../common/SaveButton/SaveButton";
let ChooseModal = (props) => {
    let [selected, setSelected] = useState(1);
    let options = props.komaxList.map(komax => komax.number).map(komax => {
        return (
            <option value={komax}>{komax}</option>
        )
    });

    let handleChoose = (e) => {
        setSelected(e.currentTarget.value);
    }

    let choose = () => {
        props.chooseKomax(props.login, selected);
        props.close();
    }
    return(
        <div className={classes.form}>
            <div className={classes.heading}>Choose komax</div>
            <select onChange={handleChoose} className={classes.select}>
                {options}
            </select>
            <div className={classes.btns}>
                <SaveButton click={choose} disable={props.komax} class={classes.save} value={"Choose"}/>
                {props.komax
                    ? <button onClick={props.close} className={classes.closeBtn}>Close</button>
                    : <></>
                }
            </div>
        </div>
    )
}

export default ChooseModal;