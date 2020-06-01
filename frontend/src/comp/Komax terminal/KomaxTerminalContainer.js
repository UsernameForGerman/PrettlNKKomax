import KomaxTerminal from "./KomaxTerminal";
import React, {useEffect, useState} from "react";
import KomaxTerminalTableItem from "./KomaxTerminalTable/Item/KTTItem";
import createTerminal from "../../DAL/models/terminal";
import komax_terminal_api from "../../DAL/komax_terminal/komax_terminal_api";
import komax_seal_api from "../../DAL/komax_seal/komax_seal_api";
import auth from "../AuthHOC/authHOC";
import TerminalSelector from "../../selectors/terminalSelector";
import {connect} from "react-redux";
import Preloader from "../common/Preloader/Preloader";
import {getTerminalListThunk} from "../../reducers/komaxTerminalReducer";
import FullScreenPreloader from "../common/Preloader/FullScreenPreloader";

let KomaxTerminalContainer = (props) => {
    const [selectedTerminal, setSelectedTerminal] = useState();
    const [materialValue, setMaterialValue] = useState();
    const [terminalAvaliable, setTerminalAvaliable] = useState();
    const [isModalOpen, setIsModalOpen] = useState(false);

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
        debugger;
        let select = () => {
            setSelectedTerminal(item);
            setMaterialValue(item.material_avaliable);
            setTerminalAvaliable(item.terminal_avaliable);
            openModal();
        }
        return (
            <KomaxTerminalTableItem {...item} select={select}/>
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
        }
    }
}

export default auth(connect(mapStateToProps, mapDispatchToProps)(KomaxTerminalContainer));