import React from "react";
import classes from "./Feedback.module.css";
import arrow from "../../../assets/images/down-arrow.png";

let Feedback = (props) => {
    return(
        <section className={classes.Feedback}>
            <div className={classes.heading}>
                <div className={classes.heading_item}>
                    Хочешь создать цифрового двойника?
                </div>
                <div className={classes.heading_item}>
                    Пиши
                </div>
            </div>
            <img src={arrow} alt={"arrow"} className={classes.arrow}/>
            <form className={classes.form}>
                <input type={"text"} name={"contacts"} className={classes.input} placeholder={"E-mail/телефон"}/>
                <button type={"submit"} className={classes.submit_btn}>Отправить</button>
            </form>
        </section>
    )
}

export default Feedback;