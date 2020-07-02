import TaskCreateModalForm from "./TCPModal";
import React, {useState} from "react";
import TerminalSelector from "../../../../selectors/terminalSelector";
import SealSelector from "../../../../selectors/sealSelector";
import {connect} from "react-redux";
import {updateTerminalThunk} from "../../../../reducers/komaxTerminalReducer";
import {updateSealThunk} from "../../../../reducers/sealReducer";
import classes from "./TCPModal.module.css"
import SealItem from "./SealItem";
import TerminalItem from "./TerminalItem";

let TaskCreateModalFormContainer = (props) => {
    let seal_list = (
        <div className={classes.list}>
            <h2 className={classes.list_heading}>Seals</h2>
            <div className={classes.table}>
                {(
                    <div className={classes.row}>
                        <div className={classes.item}>
                            <b>Seal name</b>
                        </div>
                        <div className={classes.item}>
                            <b>Seal available</b>
                        </div>
                    </div>
                )}
                {props.seals.map(seal => {
                    return <SealItem {...seal} callback={props.updateSeal}/>
                })}
            </div>
        </div>
    )

    let terminal_list = (
        <div className={classes.list}>
            <h2 className={classes.list_heading}>Terminals</h2>
            <div className={classes.table}>
                {(
                    <div className={classes.row}>
                        <div className={classes.item}>
                            <b>Terminal name</b>
                        </div>
                        <div className={classes.item}>
                            <b>Terminal available</b>
                        </div>
                    </div>
                )}
                {props.terminals.map(terminal => {
                    return <TerminalItem {...terminal} updateTerminal={props.updateTerminal}/>
                })}
            </div>
        </div>
    )

    return (
        <TaskCreateModalForm seal_list={seal_list} terminal_list={terminal_list} {...props}/>
    )
}

let mapStateToProps = (state) => {
    return {
        terminals : TerminalSelector.getList(state),
        seals : SealSelector.getList(state)
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        updateTerminal : (terminal) => {
            dispatch(updateTerminalThunk(terminal))
        },

        updateSeal : (seal) => {
            dispatch(updateSealThunk(seal))
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(TaskCreateModalFormContainer);