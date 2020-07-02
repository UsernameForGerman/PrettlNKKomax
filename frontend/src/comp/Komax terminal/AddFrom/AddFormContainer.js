import React, {useState} from "react";
import AddForm from "./AddForm";
import {createTerminalThunk} from "../../../reducers/komaxTerminalReducer";
import {connect} from "react-redux";

let AddFormContainer = (props) => {
    let [materialValue, setMaterial] = useState("False");
    let [terminalAvaliable, setTerminal] = useState("False");
    let create = (number) => {
        props.create({
            terminal_name : number,
            terminal_available : terminalAvaliable,
            seal_installed : materialValue
        })
    }
    return(
        <AddForm
            materialValue={materialValue}
            setMaterial={setMaterial}
            terminalAvaliable={terminalAvaliable}
            setTerminal={setTerminal}
            create={create}
        />
    )
}

let mapStateToProps = (state) => {
    return {

    }
}

let mapDispatchToProps = (dispatch) => {
    return{
        create : (terminal) => {
            dispatch(createTerminalThunk(terminal))
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(AddFormContainer);