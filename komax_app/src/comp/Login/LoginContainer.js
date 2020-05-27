import React from "react";
import Login from "./Login";
import LoginSelector from "../../selectors/loginSelector";
import {authThunk} from "../../reducers/loginReducer";
import {connect} from "react-redux";

let LoginContainer = (props) => {
    return(
        <Login login={props.login}/>
    );
}

let mapStateToProps = (state) => {
    return {
        isLogged : LoginSelector.getLogged(state),
        isFetching : LoginSelector.getFetching(state)
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