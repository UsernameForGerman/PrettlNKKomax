import komaxApi from "../DAL/komax/komax-api";

const initialState = {
    isFetching : false,
    komaxList : []
}

const TOGGLE_FETCHING = "KOMAX/TOGGLE_FETCHING";
const SET_LIST = "KOMAX/TOGGLE_SET_LIST";

const komaxReducer = (state = initialState, action) => {
    let stateCopy = {...state};
    switch (action.type) {
        case TOGGLE_FETCHING : {
            stateCopy.isFetching = !stateCopy.isFetching;
            break;
        }

        case SET_LIST : {
            stateCopy.komaxList = action.list;
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

const getListThunk = () => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        komaxApi.getKomaxList().then((data) => {
            dispatch(setListAC(data));
            dispatch(toggleFetchAC());
        });
    }
}

const createKomaxThunk = (komax) => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        komaxApi.createKomax(komax).then((data) => {
            dispatch(getListThunk());
            dispatch(toggleFetchAC());
        });
    }
}

const updateKomaxThunk = (komax) => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        komaxApi.updateKomax(komax).then((data) => {
            dispatch(getListThunk());
            dispatch(toggleFetchAC());
        });
    }
}

export {toggleFetchAC, setListAC, komaxReducer, getListThunk, createKomaxThunk, updateKomaxThunk};