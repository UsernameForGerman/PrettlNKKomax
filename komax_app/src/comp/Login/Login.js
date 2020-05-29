import React from "react";
import classes from "./Login.module.css"

let Login = (props) => {
    let loginRef = React.createRef();
    let passwordRef = React.createRef();
    return(
        <main className={classes.login}>
            <form>
                <input type={"text"} ref={loginRef}/>
                <input type={"password"} ref={passwordRef}/>
                <button onClick={(e) => {
                    e.preventDefault();
                    props.login(
                      loginRef.current.value,
                      passwordRef.current.value
                    );
                }}/>
            </form>
        </main>
    )
}

export default Login;
