import React, {useState} from "react";
import classes from "./KomaxTerminal.module.css"
import Modal from "react-modal";
import ModalFormContainer from "./Modal/ModalFormContainer";
import KomaxTerminalsTableContainer from "./KomaxTerminalTable/KomaxTerminalTableContainer";
import {FormattedMessage} from "react-intl";
import AddFormContainer from "./AddFrom/AddFormContainer";
import SuccessButton from "../common/SuccessButton/SuccessButton";
import SealsContainer from "../Seals/SealsContainer";

let KomaxTerminal = (props) => {

    const customStyles = {
      content : {
        top                   : '45%',
        left                  : '80%',
        transform             : 'translate(-220%, -50%)'
      }
    };

    return(
        <div className={classes.KomaxTerminal}>
            <div className={classes.cards}>
                <div className={`${classes.card} ${classes.left_card}`}>
                    <div className={classes.title}>
                        <b><FormattedMessage id={"terminal.heading"}/></b>
                    </div>
                    <SuccessButton class={classes.succBtn} click={props.openCreate} value={<FormattedMessage id={"add_button_text"}/>}/>
                    <KomaxTerminalsTableContainer items={props.items}/>
                </div>
                <div className={`${classes.card} ${classes.right_card}`}>
                    <SealsContainer/>
                </div>
            </div>
            <Modal
              isOpen={props.isModalOpen}
              onRequestClose={props.closeModal}
              style={customStyles}
              contentLabel="Example Modal"
            >
                <ModalFormContainer close={props.closeModal} isFetching={false} isValid={true} numberErrMsg={""} send={props.updateTerminal} selected={props.selected}/>
            </Modal>
            <Modal
              isOpen={props.isCreateOpen}
              onRequestClose={props.closeCreate}
              style={customStyles}
              contentLabel="Example Modal"
            >
                <AddFormContainer/>
            </Modal>
        </div>
    );
}

export default KomaxTerminal;