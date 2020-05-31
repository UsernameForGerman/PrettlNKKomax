import LabourPage from "./LabourPage";
import React, {useEffect} from "react";
import auth from "../AuthHOC/authHOC";
import classes from "./LabourPage.module.css";
import {connect} from "react-redux";
import LabourSelector from "../../selectors/labourSelector";
import {getListThunk} from "../../reducers/labourReducer";
import Preloader from "../Preloader/Preloader";

let LabourPageContainer = (props) => {
    useEffect(() => {
        props.fetchList();
    }, props.labourList);
    let items = props.labourList.map(elem => {
        return(
            <div className={classes.data_row}>
                <div className={classes.data}>
                    {elem.action}
                </div>
                <div className={classes.data}>
                    {elem.time}
                </div>
                <div className={classes.data}>
                    <button className={classes.edit_btn}>
                        Edit
                    </button>
                </div>
            </div>
        )
    })
    return(
        <>
            {props.isFetching
                ? <Preloader/>
                : <LabourPage rows={items}/>
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