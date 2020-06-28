import LabourCreateModal from "./LabourCreateModal";
import React from "react";
import {createLabourThunk, labourReducer, updateLabourThunk} from "../../../../reducers/labourReducer";
import LabourSelector from "../../../../selectors/labourSelector";
import {connect} from "react-redux";

let LabourCreateModalContainer = (props) => {
    let createLabour = (labour) => {
        let filetered = props.labourList.filter(item => item.action === labour.action);
        if (!filetered){
            props.createLabour(labour);
        }
    }
    return(
        <LabourCreateModal {...props} createLabour={createLabour}/>
    )
}
let mapStateToProps = (state) => {
    return {
        labourList : LabourSelector.getList(state)
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        createLabour : (labour) => {
            dispatch(createLabourThunk(labour))
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(LabourCreateModalContainer);