import classes from "./SealsPage.module.css";
import React, {useState} from "react";
import Modal from "react-modal";
import SealItem from "../Tasks/CreateTaskPage/Modal/SealItem";
import SuccessButton from "../common/SuccessButton/SuccessButton";
import SaveButton from "../common/SaveButton/SaveButton";
import AddForm from "./AddForm/AddForm";
import AddFormContainer from "./AddForm/AddFormContainer";
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
          <div className={classes.heading}>Seals</div>
         <div className={classes.list}>
             <SuccessButton value={"Create"} class={classes.create} click={props.openCreate}/>
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
                <>
                    <div className={classes.heading}>
                        Edit Seal
                    </div>
                    <SealItem {...props.selectedSeal} callback={setSelected}/>
                    <SaveButton click={handleClose} value={"Save"} class={classes.save}/>
                </>
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