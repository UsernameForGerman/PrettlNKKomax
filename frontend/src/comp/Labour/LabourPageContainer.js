import LabourPage from "./LabourPage";
import React, {useEffect, useState} from "react";
import auth from "../AuthHOC/authHOC";
import classes from "./LabourPage.module.css";
import {connect} from "react-redux";
import LabourSelector from "../../selectors/labourSelector";
import {getListThunk} from "../../reducers/labourReducer";
import FullScreenPreloader from "../common/Preloader/FullScreenPreloader";
import LabourItem from "./LabourItem/LabourItem";

let LabourPageContainer = (props) => {
    useEffect(() => {
        props.fetchList();
    }, props.labourList.length);
    let [selectedLabour, setSelected] = useState({});
    let [isOpenEdit, setOpenEdit] = useState(false);
    let [isCreateOpen, setCreateOpen] = useState(false);
    let items = props.labourList.map(elem => {
        let select = () => {
            setSelected(elem);
            setOpenEdit(true);
        }
        return(
            <LabourItem {...elem} select={select}/>
        )
    });
    let closeEdit = () => {
        setOpenEdit(false);
    }
    let openEdit = () => {
        setOpenEdit(true);
    }
    let openCreate = () => {
        setCreateOpen(true);
    }
    let closeCreate = () => {
        setCreateOpen(false);
    }
    return(
        <>
            {props.isFetching
                ? <FullScreenPreloader/>
                : <LabourPage
                    rows={items}
                    selectedLabour={selectedLabour}
                    isOpenEdit={isOpenEdit}
                    openEdit={openEdit}
                    closeEdit={closeEdit}
                    isCreateOpen={isCreateOpen}
                    openCreate={openCreate}
                    closeCreate={closeCreate}
                />
            }
        </>
    )
}

let mapStateToProps = (state) => {
    return {
        isFetching : LabourSelector.getFetching(state),
        labourList : LabourSelector.getList(state)
    }
}

let mapDispatchToProps = (dispatch) => {
    return{
        fetchList : () => {
            dispatch(getListThunk())
        }
    }
}


export default auth(connect(mapStateToProps, mapDispatchToProps)(LabourPageContainer));