import harnessApi from "../DAL/harness/harnessApi";
import harness_chart_api from "../DAL/harness_chart/harness_chart_api";

let initialState = {
    isFetching : false,
    harnessesList : [],
    isMapFetching : false,
    selectedMap : []
}

const TOGGLE_FETCHING = "HARNESS/FETCHING";
const TOGGLE_MAP_FETCHING = "HARNESS/MAP_FETCHING";
const SET_HARNESSES_LIST = "HARNESS/SET_LIST";
const SET_SELECTED_MAP = "HARNESS/SET_MAP";

let harnessesReducer = (state = initialState, action) => {
    let stateCopy = {...state};
    switch (action.type) {
        case TOGGLE_FETCHING : {
            stateCopy.isFetching = !stateCopy.isFetching;
            break;
        }
        case TOGGLE_MAP_FETCHING : {
            stateCopy.isMapFetching = !stateCopy.isMapFetching;
            break;
        }
        case SET_HARNESSES_LIST : {
            stateCopy.harnessesList = action.list;
            break;
        }
        case SET_SELECTED_MAP : {
            stateCopy.selectedMap = action.map;
            break;
        }
    }

    return stateCopy;
}

let toggleFetchingAC = () => {
    return {
        type : TOGGLE_FETCHING
    }
}

let toggleMapFetchingAC = () => {
    return {
        type : TOGGLE_MAP_FETCHING
    }
}

let setListAC = (list) => {
    return {
        type : SET_HARNESSES_LIST,
        list : list
    }
}

let setMapAC = (map) => {
    return {
        type : SET_SELECTED_MAP,
        map : map
    }
}

let getHarnessesListThunk = () => {
    return (dispatch) => {
        dispatch(toggleFetchingAC());
        harnessApi.getHarnessList().then(data => {
            dispatch(setListAC(data));
            dispatch(toggleFetchingAC());
        })
    }
}

let getChartByNumberThunk = (number) => {
    return (dispatch) => {
        dispatch(toggleMapFetchingAC());
        harness_chart_api.getHarnessChartByNumber(number).then(data => {
            dispatch(setMapAC(data));
            dispatch(toggleMapFetchingAC());
        });
    }
}

let deleteHarnessByNumberThunk = (number) => {
    return (dispatch) => {
        dispatch(toggleFetchingAC());
        harnessApi.deleteHarnessByNumber(number).then(data => {
            dispatch(toggleFetchingAC());
            dispatch(getHarnessesListThunk());
        });
    }
}

export {harnessesReducer, getHarnessesListThunk, deleteHarnessByNumberThunk, getChartByNumberThunk}