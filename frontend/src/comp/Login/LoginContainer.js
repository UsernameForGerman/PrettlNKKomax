import React from "react";
import Login from "./Login";
import LoginSelector from "../../selectors/loginSelector";
import {authThunk} from "../../reducers/authReducer";
import {connect} from "react-redux";
import {Redirect} from "react-router-dom";

let LoginContainer = (props) => {
    return(
        <>
            {props.isLogged
                ? <Redirect to={"/account"}/>
                : <Login login={props.login} errMsg={props.errMsg} isFetching={props.isFetching}/>
            }
        </>
    );
}

let mapStateToProps = (state) => {
    return {
        isLogged : LoginSelector.getLogged(state),
        isFetching : LoginSelector.getFetching(state),
        errMsg : LoginSelector.getErr(state)
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        login : (login, password) => {
            dispatch(authThunk(login, password))
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(LoginContainer);