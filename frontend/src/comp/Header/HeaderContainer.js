import Header from "./Header";
import React from "react";
import LoginSelector from "../../selectors/loginSelector";
import {connect} from "react-redux";
import {logoutThunk} from "../../reducers/authReducer";

let HeaderContainer = (props) => {
    return(
        <Header {...props}/>
    )
}

let mapStateToProps = (state) => {
    return {
        isLogged : LoginSelector.getLogged(state)
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        logout : () => {
            dispatch(logoutThunk())
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(HeaderContainer)