import ChooseModal from "./ChooseModal";
import React from "react";
import LoginSelector from "../../../selectors/loginSelector";
import {chooseKomaxThunk} from "../../../reducers/authReducer";
import {connect} from "react-redux";

let ChooseModalContainer = (props) => {

    return (
        <ChooseModal {...props}/>
    )
}

let mapStateToProps = (state) => {
    return {
        login : LoginSelector.getLogin(state),
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        chooseKomax : (login, komax) => {
            dispatch(chooseKomaxThunk(login, komax))
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(ChooseModalContainer);