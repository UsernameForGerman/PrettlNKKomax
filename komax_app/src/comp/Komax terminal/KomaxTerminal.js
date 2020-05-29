import React, {useState} from "react";
import classes from "./KomaxTerminal.module.css"
import KomaxTerminalEditForm from "./KTEditForm/KomaxTerminalEditForm";
import Modal from "react-modal";
import ModalFormContainer from "./Modal/ModalFormContainer";
import SuccessButton from "../common/SuccessButton/SuccessButton";
import KomaxTerminalsTableContainer from "./KomaxTerminalTable/KomaxTerminalTableContainer";
import {FormattedMessage} from "react-intl";

let KomaxTerminal = (props) => {
    let [isModalOpen, setIsModalOpen] = useState(false);

    const customStyles = {
      content : {
        top                   : '45%',
        left                  : '80%',
        transform             : 'translate(-220%, -50%)'
      }
    };

    let closeModal = (e) => {
        setIsModalOpen(false);
    }

    let openModal = (e) => {
        setIsModalOpen(true);
    }
    return(
        <div className={classes.KomaxTerminal}>
            <div className={classes.cards}>
                <div className={`${classes.card} ${classes.left_card}`}>
                    <KomaxTerminalsTableContainer items={props.items}/>
                </div>
                <div className={`${classes.card} ${classes.right_card}`}>
                    <div className={classes.heading}>
                        <div className={classes.title}>
                            <b><FormattedMessage id={"terminal.heading"}/></b>
                        </div>
                        <SuccessButton class={classes.succBtn} click={openModal} value={"+"}/>
                    </div>
                    {props.selected
                        ? <KomaxTerminalEditForm {...props}/>
                        : <div className={classes.choose}>
                            <b><FormattedMessage id={"terminal.choose_terminal"}/></b>
                          </div>
                    }
                </div>
            </div>
            <Modal
              isOpen={isModalOpen}
              onRequestClose={closeModal}
              style={customStyles}
              contentLabel="Example Modal"
            >
                <ModalFormContainer close={closeModal} isFetching={false} isValid={true} numberErrMsg={""} send={console.log}/>
            </Modal>
        </div>
    );
}

export default KomaxTerminal;