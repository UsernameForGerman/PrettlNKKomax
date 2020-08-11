import LabourEditModal from "./LabourEditModal";
import React from "react";
import {updateLabourThunk} from "../../../../reducers/labourReducer";
import LabourSelector from "../../../../selectors/labourSelector";
import {connect} from "react-redux";

let LabourEditModalContainer = (props) => {
    return(
        <LabourEditModal {...props}/>
    )
}

let mapStateToProps = (state) => {
    return {

    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        updateLabour : (labour) => {
            dispatch(updateLabourThunk(labour))
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(LabourEditModalContainer);