import labourApi from "../DAL/labour/labour_api";

const initialState = {
    isFetching : false,
    labourList : []
}

const TOGGLE_FETCHING = "LABOUR/TOGGLE_FETCHING";
const SET_LIST = "LABOUR/TOGGLE_SET_LIST";

const labourReducer = (state = initialState, action) => {
    let stateCopy = {...state};
    switch (action.type) {
        case TOGGLE_FETCHING : {
            stateCopy.isFetching = !stateCopy.isFetching;
            break;
        }

        case SET_LIST : {
            stateCopy.labourList = action.list;
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
        debugger;
        labourApi.getLabourList().then((data) => {
            debugger;
            dispatch(setListAC(data));
            dispatch(toggleFetchAC());
        });
    }
}

const createLabourThunk = (labour) => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        labourApi.createLabour(labour).then((data) => {
            dispatch(getListThunk());
            dispatch(toggleFetchAC());
        });
    }
}

const updateLabourThunk = (labour) => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        labourApi.updateLabour(labour).then((data) => {
            dispatch(getListThunk());
            dispatch(toggleFetchAC());
        });
    }
}

export {labourReducer, getListThunk, createLabourThunk, updateLabourThunk}