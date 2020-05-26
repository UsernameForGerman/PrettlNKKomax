let initialState = {
    isFetching : false,
    harnessesList : [],
    selectedMap : []
}

const TOGGLE_FETCHING = "HARNESS/FETCHING"; 
const SET_HARNESSES_LIST = "HARNESS/SET_LIST";
const SET_SELECTED_MAP = "HARNESS/SET_MAP";

let harnessesReducer = (state = initialState, action) => {
    let stateCopy = {...state};
    switch (action.type) {
        case TOGGLE_FETCHING : {
            stateCopy.isFetching = !stateCopy.isFetching;
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

let setListAC = (list) => {
    return {
        type : SET_HARNESSES_LIST,
        list : list
    }
}

let setMap = (map) => {
    return {
        type : SET_SELECTED_MAP,
        map : map
    }
}

export {harnessesReducer}