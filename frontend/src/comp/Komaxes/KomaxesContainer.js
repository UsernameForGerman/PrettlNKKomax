import {connect} from "react-redux";
import KomaxSelector from "../../selectors/komaxSelector";
import {createKomaxThunk, getListThunk, getStatusesThunk, updateKomaxThunk} from "../../reducers/komaxReducer";
import React, {useEffect, useState} from "react";
import Komaxes from "./Komaxes";
import auth from "../AuthHOC/authHOC";
import classes from "./Komaxes.module.css";
import komax from "../../assets/images/komax.png";
import FullScreenPreloader from "../common/Preloader/FullScreenPreloader";
import KappaSelector from "../../selectors/kappaSelector";
import {getKappasThunk, updateKappaThunk} from "../../reducers/kappasReducer";

let KomaxesContainer = (props) => {
    useEffect(() => {
        if(props.komaxList.length === 0){
             props.fetchKomaxes();
        }

        props.getStatuses();
    }, props.komaxList.length);

    useEffect(() => {
        props.fetchKappas();
    }, [props.kappaList.length])

    let [selectedKomax, setSelectedKomax] = useState({});

    let save = (komax) => {
        props.createKomax(komax);
    }

    let update = (komax) => {
        props.updateKomax(komax);
    }

    let statusDict = {};
    props.statuses.forEach(status => {
        statusDict[status.komax] = status.task_personal;
    });

    let getColorByNumber = (number) => {
        let status = statusDict[number];
        if (status === undefined) return "white";
        if (status === null) return "red";
        return "green";
    }

    let renderedKomaxItems = props.komaxList.map((elem) => {
        return (
            <div className={classes.komaxItem}>
                <div className={classes.komaxItemId}>
                    {elem.number}
                </div>
                <img style={{backgroundColor : getColorByNumber(elem.number)}} src={komax} alt={"komax"} className={classes.komaxImg}/>
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
                    updateKappa={props.updateKappa}
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
        komaxList : KomaxSelector.getList(state),
        kappaList : KappaSelector.getList(state),
        statuses : KomaxSelector.getStatuses(state)
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        getStatuses : () => {
            dispatch(getStatusesThunk())
        },

        fetchKomaxes : () => {
            dispatch(getListThunk())
        },

        fetchKappas : () => {
            dispatch(getKappasThunk())
        },

        createKomax : (komax) => {
            dispatch(createKomaxThunk(komax))
        },

        updateKomax : (komax) => {
            dispatch(updateKomaxThunk(komax))
        },

        updateKappa : (kappa) => {
            dispatch(updateKappaThunk(kappa))
        }
    }
}

export default auth(connect(mapStateToProps, mapDispatchToProps)(KomaxesContainer));