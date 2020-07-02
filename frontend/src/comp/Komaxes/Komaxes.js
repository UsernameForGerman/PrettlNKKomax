import classes from "./Komaxes.module.css"
import React, {useState} from "react";

import KomaxTable from "./KomaxTable/KomaxTable";
import Modal from 'react-modal';
import ModalFormContainer from "./Modal/ModalFormContainer";
import SuccessButton from "../common/SuccessButton/SuccessButton";
import {FormattedMessage} from "react-intl";

let Komaxes = (props) => {
    const customStyles = {
      content : {
        top                   : '33%',
        left                  : '60%',
        transform             : 'translate(-70%, -20%)'
      }
    };

    let [isModalOpen, setIsOpen] = useState(false);
    let openModal = () => {
        setIsOpen(true);
    }
    let closeModal = () => {
        setIsOpen(false)
    }
    let [isModalOpen2, setIsOpen2] = useState(false);
    let openModal2 = () => {
        setIsOpen2(true);
    }
    let closeModal2 = () => {
        setIsOpen2(false)
    }

    return(
      <div className={classes.Komaxes}>
          <div className={classes.container}>
            <div className={classes.komaxesColumn}>
                <SuccessButton click={openModal} value={<FormattedMessage id={"add_button_text"}/>}/>
                {props.items}
            </div>
            <div className={classes.table}>
                <KomaxTable items={props.komaxList} setSelected={props.setSelected} open={openModal2}/>
            </div>
            <Modal
              isOpen={isModalOpen}
              onRequestClose={closeModal}
              style={customStyles}
              contentLabel="Example Modal"
            >
                <ModalFormContainer close={closeModal} send={props.save} heading={<FormattedMessage id={"komax.modal_form_heading_create"}/>}/>
            </Modal>
            <Modal
              isOpen={isModalOpen2}
              onRequestClose={closeModal2}
              style={customStyles}
              contentLabel="Example Modal"
            >
                <ModalFormContainer close={closeModal2} send={props.update} selected={props.selectedKomax} heading={<FormattedMessage id={"komax.modal_form_heading_edit"}/>}/>
            </Modal>
          </div>
      </div>
    );
}

export default Komaxes;