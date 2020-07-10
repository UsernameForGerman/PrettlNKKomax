import kappa_api from "../DAL/kappa/kappa-api";
import handle401 from "./handle401";
const initialState = {
    isFetching : false,
    kappasList : []
}

const TOGGLE_FETCHING = "KAPPA/TOGGLE_FETCHING";
const SET_LIST = "KAPPA/TOGGLE_SET_LIST";

const kappasReducer = (state = initialState, action) => {
    let stateCopy = {...state};
    switch (action.type) {
        case TOGGLE_FETCHING : {
            stateCopy.isFetching = !stateCopy.isFetching;
            break;
        }

        case SET_LIST : {
            stateCopy.kappasList = action.list;
            break;
        }
    }
    return stateCopy;
}

const toggleFetchAC = () => {
    return {
        type : TOGGLE_FETCHING
    }
}

const setListAC = (list) => {
    return {
        type : SET_LIST,
        list : list
    }
}

const getKappasThunk = () => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        kappa_api.getKappaList()
            .then((data) => {
                dispatch(setListAC(data));
                dispatch(toggleFetchAC());
            })
            .catch(err => {
                handle401(err, dispatch)
            });
    }
}

const createKappaThunk = (task) => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        kappa_api.createKappa(task)
            .then((data) => {
                dispatch(getKappasThunk());
                dispatch(toggleFetchAC());
            })
            .catch(err => {
                handle401(err, dispatch)
            });
    }
}

export {kappasReducer, getKappasThunk, createKappaThunk}