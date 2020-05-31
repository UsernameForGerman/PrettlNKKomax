import {connect} from "react-redux";
import KomaxSelector from "../../selectors/komaxSelector";
import {createKomaxThunk, getListThunk, updateKomaxThunk} from "../../reducers/komaxReducer";
import React, {useEffect, useState} from "react";
import Komaxes from "./Komaxes";
import auth from "../AuthHOC/authHOC";
import classes from "./Komaxes.module.css";
import komax from "../../assets/images/komax.png";
import file from "../../assets/docs/6282-2124813-12.xlsx"
import harnessApi from "../../DAL/harness/harness-api";
import Preloader from "../common/Preloader/Preloader";
import FullScreenPreloader from "../common/Preloader/FullScreenPreloader";

let KomaxesContainer = (props) => {
    useEffect(() => {
        if(props.komaxList.length === 0){
             props.fetchKomaxes();
        }
    }, props.komaxList);

    let [selectedKomax, setSelectedKomax] = useState({});

    let save = (komax) => {
        props.createKomax(komax);
    }

    let update = (komax) => {
        props.updateKomax(komax);
    }

    let renderedKomaxItems = props.komaxList.map((elem) => {
        return (
            <div className={classes.komaxItem}>
                <div className={classes.komaxItemId}>
                    {elem.number}
                </div>
                <img src={komax} alt={"komax"} className={classes.komaxImg}/>
            </div>
        );
    });

    return(
        <>
            {props.isFetching
                ? <FullScreenPreloader/>
                : <Komaxes
                    {...props}
                    items={renderedKomaxItems}
                    save={save}
                    update={update}
                    selectedKomax={selectedKomax}
                    setSelected={setSelectedKomax}
                />
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
        },

        createKomax : (komax) => {
            dispatch(createKomaxThunk(komax))
        },

        updateKomax : (komax) => {
            dispatch(updateKomaxThunk(komax))
        }
    }
}

export default auth(connect(mapStateToProps, mapDispatchToProps)(KomaxesContainer));