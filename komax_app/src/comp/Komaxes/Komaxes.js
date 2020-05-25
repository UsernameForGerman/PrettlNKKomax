import classes from "./Komaxes.module.css"
import React, {useState} from "react";

import komax from "../../assets/images/komax.png"
import Table from "../Table/Table";
import Modal from 'react-modal';
import ModalForm from "./Modal/ModalForm";

let Komaxes = (props) => {
    const customStyles = {
      content : {
        top                   : '10%',
        left                  : '30%',
        transform             : 'translate(-10%, -5%)'
      }
    };

    let [selectedKomax, setSelectedKomax] = useState({});

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
                <div className={classes.komaxItem}>
                    <div className={classes.komaxItemId}>
                        1
                    </div>
                    <img src={komax} alt={"komax"} className={classes.komaxImg}/>
                </div>
                <div className={classes.komaxItem}>
                    <div className={classes.komaxItemId}>
                        2
                    </div>
                    <img src={komax} alt={"komax"} className={classes.komaxImg}/>
                </div>
                <div className={classes.komaxItem}>
                    <div className={classes.komaxItemId}>
                        3
                    </div>
                    <img src={komax} alt={"komax"} className={classes.komaxImg}/>
                </div>
                <div className={classes.komaxItem}>
                    <div className={classes.komaxItemId}>
                        4
                    </div>
                    <img src={komax} alt={"komax"} className={classes.komaxImg}/>
                </div>
                <div className={classes.komaxItem}>
                    <div className={classes.komaxItemId}>
                        5
                    </div>
                    <img src={komax} alt={"komax"} className={classes.komaxImg}/>
                </div>
            </div>
            <div className={classes.table}>
                <Table items={props.komaxList} setSelected={setSelectedKomax} open={openModal2}/>
            </div>
            <Modal
              isOpen={isModalOpen}
              onRequestClose={closeModal}
              style={customStyles}
              contentLabel="Example Modal"
            >
                <ModalForm close={closeModal} heading={"Cоздать новый аппарат"}/>
            </Modal>
            <Modal
              isOpen={isModalOpen2}
              onRequestClose={closeModal2}
              style={customStyles}
              contentLabel="Example Modal"
            >
                <ModalForm close={closeModal2} selected={selectedKomax} heading={"Изменить существующий аппарат"}/>
            </Modal>
          </div>
      </div>
    );
}

export default Komaxes;