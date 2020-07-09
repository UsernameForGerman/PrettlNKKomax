import classes from "./ChooseModal.module.css";
import React, {useState} from "react";
import SaveButton from "../../common/SaveButton/SaveButton";
import {FormattedMessage} from "react-intl";
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
            <div className={classes.heading}><FormattedMessage id={"choose_komax_label"}/></div>
            <select onChange={handleChoose} className={classes.select}>
                {options}
            </select>
            <div className={classes.btns}>
                <SaveButton click={choose} disable={props.komax} class={classes.save} value={<FormattedMessage id={"choose_label"}/>}/>
                {props.komax
                    ? <button onClick={props.close} className={classes.closeBtn}><FormattedMessage id={"close_label"}/></button>
                    : <></>
                }
            </div>
        </div>
    )
}

export default ChooseModal;