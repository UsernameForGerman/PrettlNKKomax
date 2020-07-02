import StartPage from "./StartPage";
import React, {useEffect, useState} from "react";
import auth from "../AuthHOC/authHOC";
import ava from "../../assets/images/ava.png"
import Modal from 'react-modal';
import {connect} from "react-redux";
import LoginSelector from "../../selectors/loginSelector";
import {chooseKomaxThunk} from "../../reducers/authReducer";
import ChooseModalContainer from "./Modal/ChooseModalContainer";
import KomaxSelector from "../../selectors/komaxSelector";
import {getListThunk} from "../../reducers/komaxReducer";
import SaveButton from "../common/SaveButton/SaveButton";
import classes from "./StartPage.module.css"

let StartPageContainer = (props) => {
    useEffect(() => {
        props.fetchKomaxes();
    }, [props.komaxList.length])

    const customStyles = {
      content : {
        top                   : '25%',
        left                  : '60%',
        transform             : 'translate(-70%, -20%)'
      }
    };

    let user = {
        username : props.login,
        role : props.role
    }

    const [isOpen, setOpen] = useState(false);
    const [isSettingsOpen, setSettingsOpen] = useState(false);

    let openModal = () => {
        setOpen(true);
    }

    let closeModal = () => {
        setOpen(false);
    }

    let openSettings = () => {
        setSettingsOpen(true);
    }

    let closeSettings = () => {
        setSettingsOpen(false);
    }

    if (props.role.toString().toLocaleLowerCase() === "operator" && props.komax === "" && !isOpen) openModal();

    return(
        <>
            <StartPage {...user} ava={ava} open={openSettings}/>
            <Modal
              isOpen={isOpen}
              style={customStyles}
              contentLabel="Example Modal"
            >
                <ChooseModalContainer komaxList={props.komaxList} close={closeModal} komax={props.komax}/>
            </Modal>
            <Modal
              isOpen={isSettingsOpen}
              style={customStyles}
              onRequestClose={closeSettings}
              contentLabel="Example Modal"
            >
                <div className={classes.choose_form}>
                    <div className={classes.choose_heading}>
                        Choose your avatar
                    </div>
                    <div className={classes.ava_block}>
                        <img src={ava} alt={"Avatar"} className={classes.choose_ava}/>
                        <input type={"file"} className={classes.input}/>
                    </div>
                    <div className={classes.btns}>
                        <SaveButton value={"Save"}/>
                        <button className={classes.close_btn} onClick={closeSettings}>Close</button>
                    </div>
                </div>
            </Modal>
        </>
    )
}

let mapStateToProps = (state) => {
    return {
        login : LoginSelector.getLogin(state),
        role : LoginSelector.getRole(state),
        komax : LoginSelector.getKomax(state),
        komaxList : KomaxSelector.getList(state),
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        choose : (login, number) => {
            dispatch(chooseKomaxThunk(login, number))
        },

        fetchKomaxes : () => {
            dispatch(getListThunk())
        }
    }
}

export default auth(connect(mapStateToProps, mapDispatchToProps)(StartPageContainer));