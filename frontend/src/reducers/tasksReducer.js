import task_api from "../DAL/task/task_api";
const initialState = {
    isFetching : false,
    tasksList : [],
    errMsg : "",
    isValid : true,
    canSend : false
}

const TOGGLE_FETCHING = "TASKS/TOGGLE_FETCHING";
const SET_LIST = "TASKS/TOGGLE_SET_LIST";
const SET_ERR_MSG = "TASKS/ERROR";
const SET_VALID = "TASKS/VALID";
const SET_CAN_SEND = "TASKS/CAN_SEND";

const tasksReducer = (state = initialState, action) => {
    let stateCopy = {...state};
    switch (action.type) {
        case TOGGLE_FETCHING : {
            stateCopy.isFetching = !stateCopy.isFetching;
            break;
        }

        case SET_LIST : {
            stateCopy.tasksList = action.list;
            break;
        }

        case SET_ERR_MSG : {
            stateCopy.errMsg = action.error;
            break;
        }

        case SET_VALID : {
            stateCopy.isValid = action.isValid;
            break;
        }

        case SET_CAN_SEND : {
            stateCopy.canSend = action.canSend;
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

const canSendAC = (send) => {
    return {
        type : SET_CAN_SEND,
        canSend : send
    }
}

const setListAC = (list) => {
    return {
        type : SET_LIST,
        list : list
    }
}

const setValidAC = (isValid) => {
    return {
        type : SET_VALID,
        isValid : isValid
    }
}

const setErrorAC = (error) => {
    return {
        type : SET_ERR_MSG,
        error : error
    }
}

const getTasksThunk = () => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        task_api.getKomaxTasks().then((data) => {
            dispatch(setListAC(data));
            dispatch(toggleFetchAC());
        });
    }
}

const createTaskThunk = (task) => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        task_api.createTask(task).then((data) => {
            dispatch(canSendAC(true));
            dispatch(toggleFetchAC());
        });
    }
}

const updateTaskThunk = (task) => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        task_api.updateTask(task).then((data) => {
            dispatch(getTasksThunk());
            dispatch(toggleFetchAC());
        });
    }
}

export {tasksReducer, createTaskThunk, updateTaskThunk, getTasksThunk, setErrorAC, setValidAC}