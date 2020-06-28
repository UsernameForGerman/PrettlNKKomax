import classes from "./LabourPage.module.css"
import React from "react";
import Modal from 'react-modal';
import LabourCreateModalContainer from "./Modal/Create/LabourCreateModalContainer";
import LabourEditModalContainer from "./Modal/Edit/LabourEditModalContainer";
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
                    Laboriousness
                </h1>
                <div className={classes.table}>
                    <button className={classes.create_btn} onClick={props.openCreate}>
                        Create
                    </button>
                    <div className={classes.table_heading}>
                        <div className={classes.data}>
                            <b>Action</b>
                        </div>
                        <div className={classes.data}>
                            <b>Time (sec)</b>
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