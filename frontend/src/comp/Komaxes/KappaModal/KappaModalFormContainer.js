import KappaModalForm from "./KappaModalForm";
import React from "react";
import {connect} from "react-redux";
import ModalSelector from "../../../selectors/modalSelector";
import {checkValidThunk} from "../../../reducers/modalReducer";

let KappaModalFormContainer = (props) => {
    return (
        <KappaModalForm {...props}/>
    );
}

let mapStateToProps = (state) => {
    return{
        isFetching : ModalSelector.getFetching(state),
        isValid : ModalSelector.getValid(state),
        numberErrMsg : ModalSelector.getNumberErrMsg(state),
        idErrMsg : ModalSelector.getIdErrMsg(state)
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        checkValid : (number) => {
            dispatch(checkValidThunk(number))
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(KappaModalFormContainer);