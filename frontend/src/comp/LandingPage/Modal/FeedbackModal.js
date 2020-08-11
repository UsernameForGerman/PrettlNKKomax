import classes from "./FeedbackModal.module.css"
import React from "react";

let FeedbackModal = (props) => {
    return (<form className={classes.form}>
                <h2>Оставьте свои контакты</h2>
                <input type={"text"} name={"contacts"} className={classes.input} placeholder={"E-mail/телефон"}/>
                <button type={"submit"} className={classes.submit_btn}>Отправить</button>
            </form>)
}

export default FeedbackModal;