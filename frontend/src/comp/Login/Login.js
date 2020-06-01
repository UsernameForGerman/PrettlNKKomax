import React from "react";
import classes from "./Login.module.css"
import {FormattedMessage} from "react-intl";

let Login = (props) => {
    let loginRef = React.createRef();
    let passwordRef = React.createRef();
    return(
        <main className={classes.login}>
            <div className={classes.heading}>
                <h1><FormattedMessage id={"login.auth_label"}/></h1>
            </div>
            <form className={classes.form}>
                <input type={"text"} ref={loginRef} className={classes.input} placeholder={"Login"}/>
                <input type={"password"} ref={passwordRef} className={classes.input} placeholder={"Password"}/>
                <button onClick={(e) => {
                    e.preventDefault();
                    props.login(
                      loginRef.current.value,
                      passwordRef.current.value
                    );
                }} className={classes.sign_in_btn} disabled={props.isFetching}><FormattedMessage id={"login.sign_in_label"}/></button>
                <div className={classes.errorBlock}>
                    {props.errMsg}
                </div>
            </form>
        </main>
    )
}

export default Login;
