import {connect} from "react-redux";
import KomaxSelector from "../../selectors/komaxSelector";
import {getListThunk} from "../../reducers/komaxReducer";
import React, {useEffect} from "react";
import Komaxes from "./Komaxes";
import classes from "./Komaxes.module.css";
import komax from "../../assets/images/komax.png";

let KomaxesContainer = (props) => {
    useEffect(() => {
        if(props.komaxList.length === 0){
             props.fetchKomaxes();
        }
    }, props.komaxList);

    let renderedKomaxItems = props.komaxList.map((elem) => {
        return (
            <div className={classes.komaxItem}>
                <div className={classes.komaxItemId}>
                    {elem.number}
                </div>
                <img src={komax} alt={"komax"} className={classes.komaxImg}/>
            </div>
        );
    })

    return(
        <>
            {props.isFetching
                ? <></>
                : <Komaxes {...props} items={renderedKomaxItems}/>
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