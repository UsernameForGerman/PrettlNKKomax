import classes from "./SealsPage.module.css";
import React, {useState} from "react";
import Modal from "react-modal";
import SealItem from "../Tasks/CreateTaskPage/Modal/SealItem";
import SuccessButton from "../common/SuccessButton/SuccessButton";
import SaveButton from "../common/SaveButton/SaveButton";
import AddForm from "./AddForm/AddForm";
import AddFormContainer from "./AddForm/AddFormContainer";
import {FormattedMessage} from "react-intl";
let SealsPage = (props) => {
    const customStyles = {
      content : {
        top                   : '60%',
        left                  : '80%',
        transform             : 'translate(-225%, -70%)'
      }
    };

    const [selected, setSelected] = useState(props.selectedSeal);

    let handleClose = () => {
        props.close();
        props.updateSeal(selected);
    }

    return (
      <div className={classes.container}>
          <div className={classes.heading}><FormattedMessage id={"seals_label"}/></div>
         <div className={classes.list}>
             <SuccessButton value={<FormattedMessage id={"add_button_text"}/>} class={classes.create} click={props.openCreate}/>
             {props.heading}
             <div className={classes.wrapper}>
                 {props.list}
             </div>
         </div>
            <Modal
              isOpen={props.isModalOpen}
              onRequestClose={props.close}
              style={customStyles}
              contentLabel="Example Modal"
            >
                <div className={classes.seal_form}>
                    <div className={classes.heading}>
                        <FormattedMessage id={"seal_edit"}/>
                    </div>
                    <SealItem {...props.selectedSeal} callback={setSelected}/>
                    <SaveButton click={handleClose} value={<FormattedMessage id={"save_button_label"}/>} class={classes.save}/>
                </div>
            </Modal>
            <Modal
              isOpen={props.isCreateOpen}
              onRequestClose={props.closeCreate}
              style={customStyles}
              contentLabel="Example Modal"
            >
                <AddFormContainer close={props.closeCreate}/>
            </Modal>
      </div>
    );
}

export default SealsPage;