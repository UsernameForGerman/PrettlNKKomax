import KomaxTerminal from "./KomaxTerminal";
import React, {useEffect, useState} from "react";
import KomaxTerminalTableItem from "./KomaxTerminalTable/Item/KTTItem";
import auth from "../AuthHOC/authHOC";
import TerminalSelector from "../../selectors/terminalSelector";
import {connect} from "react-redux";
import {deleteTerminalThunk, getTerminalListThunk, updateTerminalThunk} from "../../reducers/komaxTerminalReducer";
import FullScreenPreloader from "../common/Preloader/FullScreenPreloader";

let KomaxTerminalContainer = (props) => {
    const [selectedTerminal, setSelectedTerminal] = useState({});
    const [materialValue, setMaterialValue] = useState();
    const [terminalAvaliable, setTerminalAvaliable] = useState();
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isCreateOpen, setCreateOpen] = useState(false);

    let openCreate = (e) => {
        setCreateOpen(true);
    }

    let closeCreate = (e) => {
        setCreateOpen(false);
    }

    let closeModal = (e) => {
        setIsModalOpen(false);
    }

    let openModal = (e) => {
        setIsModalOpen(true);
    }

    useEffect(() => {
        props.fetchList();
    }, props.terminalList.length)

    let list = props.terminalList;
    if (!list){
        list = [];
    }
    let items = list.map((item) => {
        let select = () => {
            setSelectedTerminal(item);
            setMaterialValue(item.seal_installed);
            setTerminalAvaliable(item.terminal_avaliable);
            openModal();
        }

        let del = (e) => {
            e.stopPropagation();
            props.deleteTerminal(item);
        }
        return (
            <KomaxTerminalTableItem {...item} select={select} del={del}/>
        )
    })

    return(
        <>
            {props.isFetching
                ? <FullScreenPreloader/>
                : <KomaxTerminal items={items}
                       selected={selectedTerminal}
                       setMaterial={setMaterialValue}
                       setTerminal={setTerminalAvaliable}
                       terminalAvaliable={terminalAvaliable}
                       materialValue={materialValue}
                       isModalOpen={isModalOpen}
                       setIsModalOpen={setIsModalOpen}
                       closeModal={closeModal}
                       isCreateOpen={isCreateOpen}
                       openCreate={openCreate}
                       closeCreate={closeCreate}
                       updateTerminal={props.updateTerminal}
                       deleteTerminal={props.deleteTerminal}
                />
            }
        </>
    )
}

let mapStateToProps = (state) => {
    return {
        terminalList : TerminalSelector.getList(state),
        isFetching : TerminalSelector.getFetching(state)
    }
}

let mapDispatchToProps = (dispatch) => {
    return{
        fetchList : () => {
            dispatch(getTerminalListThunk())
        },

        updateTerminal : (terminal) => {
            dispatch(updateTerminalThunk(terminal))
        },

        deleteTerminal : (terminal) => {
            dispatch(deleteTerminalThunk(terminal))
        }
    }
}

export default auth(connect(mapStateToProps, mapDispatchToProps)(KomaxTerminalContainer));