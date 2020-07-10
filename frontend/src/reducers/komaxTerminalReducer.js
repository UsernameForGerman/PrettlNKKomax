import komax_terminal_api from "../DAL/komax_terminal/komax_terminal_api";
import handle401 from "./handle401";

const initialState = {
    isFetching : false,
    terminalsList : []
}

const TOGGLE_FETCHING = "TERMINAL/TOGGLE_FETCHING";
const SET_LIST = "TERMINAL/TOGGLE_SET_LIST";

const komaxTerminalReducer = (state = initialState, action) => {
    let stateCopy = {...state};
    switch (action.type) {
        case TOGGLE_FETCHING : {
            stateCopy.isFetching = !stateCopy.isFetching;
            break;
        }

        case SET_LIST : {
            stateCopy.terminalsList = action.list;
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

const getTerminalListThunk = () => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        komax_terminal_api.getTerminalList()
            .then((data) => {
                dispatch(setListAC(data));
                dispatch(toggleFetchAC());
            })
            .catch(err => {
                handle401(err, dispatch)
            });
    }
}

const createTerminalThunk = (terminal) => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        komax_terminal_api.createTerminal(terminal)
            .then((data) => {
                dispatch(getTerminalListThunk());
                dispatch(toggleFetchAC());
            })
            .catch(err => {
                handle401(err, dispatch)
            });
    }
}

const updateTerminalThunk = (terminal) => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        komax_terminal_api.updateTerminal(terminal)
            .then((data) => {
                dispatch(getTerminalListThunk());
                dispatch(toggleFetchAC());
            })
            .catch(err => {
                handle401(err, dispatch)
            });
    }
}

export {komaxTerminalReducer, updateTerminalThunk, getTerminalListThunk, createTerminalThunk}