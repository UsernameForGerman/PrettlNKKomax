import ModalForm from "./ModalForm";
import React from "react";
import {connect} from "react-redux";
import ModalSelector from "../../../selectors/modalSelector";
import {checkValidThunk} from "../../../reducers/modalReducer";

let ModalFormContainer = (props) => {
    return (
        <ModalForm {...props}/>
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
        checkValid : (number, id) => {
            dispatch(checkValidThunk(number, id))
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(ModalFormContainer);