import AddForm from "./AddForm";
import React from "react";
import {createSealThunk} from "../../../reducers/sealReducer";
import {connect} from "react-redux";
import SealSelector from "../../../selectors/sealSelector";

let AddFormContainer = (props) => {
    return (
        <AddForm {...props}/>
    )
}

let mapStateToProps = (state) => {
    return {
        sealList : SealSelector.getList(state)
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        createSeal : (seal) => {
            dispatch(createSealThunk(seal))
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(AddFormContainer);