import classes from "./Komaxes.module.css"
import React, {useState} from "react";

import komax from "../../assets/images/komax.png"
import KomaxTable from "./KomaxTable/KomaxTable";
import Modal from 'react-modal';
import ModalForm from "./Modal/ModalForm";
import ModalFormContainer from "./Modal/ModalFormContainer";

let Komaxes = (props) => {
    const customStyles = {
      content : {
        top                   : '25%',
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
                <button className={classes.succBtn} onClick={openModal}>
                    Добавить
                </button>
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
                <ModalFormContainer close={closeModal} send={props.save} heading={"Cоздать новый аппарат"}/>
            </Modal>
            <Modal
              isOpen={isModalOpen2}
              onRequestClose={closeModal2}
              style={customStyles}
              contentLabel="Example Modal"
            >
                <ModalFormContainer close={closeModal2} send={props.update} selected={props.selectedKomax} heading={"Изменить существующий аппарат"}/>
            </Modal>
          </div>
      </div>
    );
}

export default Komaxes;