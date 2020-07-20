import classes from "./LabourPage.module.css"
import React from "react";
import Modal from 'react-modal';
import LabourCreateModalContainer from "./Modal/Create/LabourCreateModalContainer";
import LabourEditModalContainer from "./Modal/Edit/LabourEditModalContainer";
import {FormattedMessage} from "react-intl";
import SuccessButton from "../common/SuccessButton/SuccessButton";
let LabourPage = (props) => {
    const customStyles = {
      content : {
        top                   : '45%',
        left                  : '60%',
        transform             : 'translate(-70%, -40%)'
      }
    };

    return(
        <div className={classes.LabourPage}>
            <div className={classes.container}>
                <h1>
                    <FormattedMessage id={"labournesses_label"}/>
                </h1>
                <div className={classes.table}>
                    <SuccessButton value={<FormattedMessage id={"add_button_text"}/>} click={props.openCreate}/>
                    <div className={classes.table_heading}>
                        <div className={classes.data}>
                            <b><FormattedMessage id={"action_label"}/></b>
                        </div>
                        <div className={classes.data}>
                            <b><FormattedMessage id={"time_label"}/></b>
                        </div>
                    </div>
                    {props.rows}
                </div>
            </div>
            <Modal
              isOpen={props.isOpenEdit}
              onRequestClose={props.closeEdit}
              style={customStyles}
              contentLabel="Example Modal"
            >
                <LabourEditModalContainer selectedLabour={props.selectedLabour} close={props.closeEdit}/>
            </Modal>
            <Modal
              isOpen={props.isCreateOpen}
              onRequestClose={props.closeCreate}
              style={customStyles}
              contentLabel="Example Modal"
             >
                <LabourCreateModalContainer close={props.closeCreate}/>
            </Modal>
        </div>
    )
}

export default LabourPage;