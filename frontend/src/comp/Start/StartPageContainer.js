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

let StartPageContainer = (props) => {
    useEffect(() => {
        props.fetchList();
    },[props.komaxList.length]);

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

    let openModal = () => {
        setOpen(true);
    }

    let closeModal = () => {
        setOpen(false);
    }

    if (props.role.toString().toLocaleLowerCase() === "operator" && props.komax === "" && !isOpen) openModal();

    return(
        <>
            <StartPage {...user} ava={ava}/>
            <Modal
              isOpen={isOpen}
              style={customStyles}
              contentLabel="Example Modal"
            >
                <ChooseModalContainer komaxList={props.komaxList} close={closeModal} komax={props.komax}/>
            </Modal>
        </>
    )
}

let mapStateToProps = (state) => {
    return {
        login : LoginSelector.getLogin(state),
        role : LoginSelector.getRole(state),
        komax : LoginSelector.getKomax(state),
        komaxList : KomaxSelector.getList(state)
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        choose : (login, number) => {
            dispatch(chooseKomaxThunk(login, number))
        },

        fetchList : () => {
            dispatch(getListThunk())
        }
    }
}

export default auth(connect(mapStateToProps, mapDispatchToProps)(StartPageContainer));