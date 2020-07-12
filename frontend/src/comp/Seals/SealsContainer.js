import React, {useEffect, useState} from "react";
import SealsPage from "./SealsPage";
import auth from "../AuthHOC/authHOC";
import {connect} from "react-redux";
import SealSelector from "../../selectors/sealSelector";
import {deleteSealThunk, getSealsListThunk, updateSealThunk} from "../../reducers/sealReducer";
import classes from "./SealsPage.module.css"
import Preloader from "../common/Preloader/Preloader";
import IconButton from "../common/IconButton/IconButton";
import {FormattedMessage} from "react-intl";

let SealsContainer = (props) => {
    useEffect(() => {
        props.getSeals();
    }, props.seals.length);

    let [selectedSeal, setSelectedSeal] = useState({});
    let [isModalOpen, setModalOpen] = useState(false);
    let [isCreateOpen, setCreateOpen] = useState(false);

    let openCreate = () => {
        setCreateOpen(true);
    }

    let closeCreate = () => {
        setCreateOpen(false);
    }

    let closeModal = () => {
        setModalOpen(false);
    }

    let renderedSeals = props.seals.map(seal => {
        let select = () => {
            setSelectedSeal(seal);
            setModalOpen(true);
        }

        let del = (e) => {
            e.stopPropagation();
            props.deleteSeal(seal);
        }

        return (
            <div className={classes.row} onClick={select}>
                <div className={classes.data}>
                    {seal.seal_name}
                </div>
                <div className={classes.data}>
                    {seal.seal_available ? "+" : "-"}
                </div>
                <IconButton icon={['fas', 'trash']} class={classes.btn} click={del}/>
            </div>
        )
    })

    let heading = (
        <div className={classes.heading_row}>
            <div className={classes.data}>
                <b className={classes.heading_text}><FormattedMessage id={"seal_name_label"}/></b>
            </div>
            <div className={classes.data}>
                <b className={classes.heading_text}><FormattedMessage id={"terminal.material_avaliable_label"}/></b>
            </div>
        </div>
    )

    return (
        <>
            <SealsPage
                list={renderedSeals}
                isModalOpen={isModalOpen}
                isCreateOpen={isCreateOpen}
                close={closeModal}
                selectedSeal={selectedSeal}
                heading={heading}
                updateSeal={props.updateSeal}
                openCreate={openCreate}
                closeCreate={closeCreate}
            />
        </>
    )
}

let mapStateToProps = (state) => {
    return {
        seals : SealSelector.getList(state),
        isFetching : SealSelector.getFetching(state)
    }
}

let mapDispatchProps = (dispatch) => {
    return {
        getSeals : () => {
            dispatch(getSealsListThunk())
        },

        updateSeal : (seal) => {
            dispatch(updateSealThunk(seal))
        },

        deleteSeal : (seal) => {
            dispatch(deleteSealThunk(seal))
        }
    }
}

export default auth(connect(mapStateToProps, mapDispatchProps)(SealsContainer));