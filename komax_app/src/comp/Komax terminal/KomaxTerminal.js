import React, {useState} from "react";
import classes from "./KomaxTerminal.module.css"
import KomaxTerminalTable from "./KomaxTerminalTable/KomaxTerminalTable";
import KomaxTerminalEditForm from "./KTEditForm/KomaxTerminalEditForm";
import Modal from "react-modal";
import ModalFormContainer from "./Modal/ModalFormContainer";

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
                    <KomaxTerminalTable items={props.items}/>
                </div>
                <div className={`${classes.card} ${classes.right_card}`}>
                    <div className={classes.heading}>
                        <div className={classes.title}>
                            <b>Komax terminals</b>
                        </div>
                        <button className={classes.succBtn} onClick={openModal}>
                            +
                        </button>
                    </div>
                    {props.selected
                        ? <KomaxTerminalEditForm {...props}/>
                        : <div className={classes.choose}>
                            <b>Выберите терминал для редактирования</b>
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