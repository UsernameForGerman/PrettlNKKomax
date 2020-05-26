import {connect} from "react-redux";
import KomaxSelector from "../../selectors/komaxSelector";
import {getListThunk} from "../../reducers/komaxReducer";
import React, {useEffect} from "react";
import Komaxes from "./Komaxes";

let KomaxesContainer = (props) => {
    useEffect(() => {
        if(props.komaxList.length === 0){
             props.fetchKomaxes();
        }
    }, props.komaxList);

    return(
        <>
            {props.isFetching
                ? <></>
                : <Komaxes {...props}/>
            }
        </>
    )
}

let mapStateToProps = (state) => {
    return {
        isFetching : KomaxSelector.getFetching(state),
        komaxList : KomaxSelector.getList(state)
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        fetchKomaxes : () => {
            dispatch(getListThunk())
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(KomaxesContainer);