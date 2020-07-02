import komax_seal_api from "../DAL/komax_seal/komax_seal_api";

const initialState = {
    isFetching : false,
    sealsList : []
}

const TOGGLE_FETCHING = "SEAL/TOGGLE_FETCHING";
const SET_LIST = "SEAL/TOGGLE_SET_LIST";

const sealReducer = (state = initialState, action) => {
    let stateCopy = {...state};
    switch (action.type) {
        case TOGGLE_FETCHING : {
            stateCopy.isFetching = !stateCopy.isFetching;
            break;
        }

        case SET_LIST : {
            stateCopy.sealsList = action.list;
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

const getSealsListThunk = () => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        komax_seal_api.getSealsList().then((data) => {
            dispatch(setListAC(data));
            dispatch(toggleFetchAC());
        });
    }
}

const updateSealThunk = (seal) => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        komax_seal_api.updateSeal(seal).then((data) => {
            dispatch(getSealsListThunk());
            dispatch(toggleFetchAC());
        });
    }
}

const createSealThunk = (seal) => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        komax_seal_api.createSeal(seal).then((data) => {
            dispatch(getSealsListThunk());
            dispatch(toggleFetchAC());
        });
    }
}

const deleteSealThunk = (seal) => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        komax_seal_api.deleteSeal(seal).then((data) => {
            dispatch(getSealsListThunk());
            dispatch(toggleFetchAC());
        });
    }
}

export {getSealsListThunk, updateSealThunk, sealReducer, createSealThunk, deleteSealThunk}