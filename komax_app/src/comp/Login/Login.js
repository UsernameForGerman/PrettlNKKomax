import React from "react";

let Login = (props) => {
    let loginRef = React.createRef();
    let passwordRef = React.createRef();
    return(
        <div>
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
        </div>
    )
}

export default Login;
