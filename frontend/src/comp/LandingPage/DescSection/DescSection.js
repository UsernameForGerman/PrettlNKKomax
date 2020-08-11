import React, {useState} from "react";
import classes from "./DescSection.module.css"
import Modal from "react-modal";
import FeedbackModal from "../Modal/FeedbackModal";

let DescSection = (props) => {
    let [isOpen, setOpen] = useState(false);
    let toggle = () => {
        setOpen(!isOpen);
    }
    const customStyles = {
      content : {
        top                   : '60%',
        left                  : '80%',
        transform             : 'translate(-225%, -70%)'
      }
    };
    return (<section className={classes.desc_section}>
                <div className={classes.desc_heading}>
                    <div className={classes.desc_heading_row}>
                        Управляй
                    </div>
                    <div className={classes.desc_heading_row}>
                        Быстрее. Дешевле. Стабильнее
                    </div>
                    <div className={classes.desc_heading_bottom}>
                         с автоматизацией и оцифровкой производственных процессов с TetraD-NK
                    </div>
                </div>
                <div className={classes.desc_btns}>
                    <button className={classes.desc_btn} onClick={toggle}>
                        Создать
                    </button>
                    <button className={classes.desc_btn} onClick={toggle}>
                        Обсудить проект
                    </button>
                </div>
                <Modal
                  isOpen={isOpen}
                  onRequestClose={toggle}
                  style={customStyles}
                  contentLabel="Example Modal"
                >
                    <FeedbackModal/>
                </Modal>
            </section>)
}

export default DescSection;