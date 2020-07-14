import task_api from "../DAL/task/task_api";
import task_status from "../DAL/task_status/task_status";
import {logoutThunk} from "./authReducer";
import handle401 from "./handle401";
const initialState = {
    isFetching : false,
    tasksList : [],
    errMsg : "",
    isValid : true,
    canSend : false,
    status : {
        harnesses : []
    }
}

const TOGGLE_FETCHING = "TASKS/TOGGLE_FETCHING";
const SET_LIST = "TASKS/TOGGLE_SET_LIST";
const SET_ERR_MSG = "TASKS/ERROR";
const SET_VALID = "TASKS/VALID";
const SET_CAN_SEND = "TASKS/CAN_SEND";
const SET_STATUS = "TASKS/SET_STATUS";

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

        case SET_STATUS : {
            stateCopy.status = action.status;
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

const setStatusAC = (status) => {
    return {
        type : SET_STATUS,
        status : status
    }
}

const getTasksThunk = () => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        task_api.getKomaxTasks().then((data) => {
            if (data === "") data = [];
            dispatch(setListAC(data));
            dispatch(toggleFetchAC());
        }).catch(err => {
            handle401(err, dispatch);
            dispatch(toggleFetchAC())
        });
    }
}

const createTaskThunk = (task) => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        task_api.createTask(task)
            .then((data) => {
                dispatch(canSendAC(true));
                dispatch(toggleFetchAC());
            })
            .catch(err => {
                handle401(err, dispatch);
            });
    }
}

const updateTaskThunk = (task) => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        task_api.updateTask(task)
            .then((data) => {
                dispatch(getTasksThunk());
                dispatch(toggleFetchAC());
            })
            .catch(err => {
                handle401(err, dispatch);
            });
    }
}

let getStatusThunk = () => {
    return (dispatch) => {
        task_status.getStatuses()
            .then(resp => {
                dispatch(setStatusAC(resp));
            })
            .catch(err => {
                handle401(err, dispatch);
            });
    }
}

let deleteTaskThunk = (task) => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        task_api.deleteTask(task)
            .then(resp => {
                dispatch(getTasksThunk());
                dispatch(toggleFetchAC());
            })
            .catch(err => {
                handle401(err, dispatch)
            })
    }
}

export {tasksReducer, createTaskThunk, updateTaskThunk, getTasksThunk, setErrorAC, setValidAC, getStatusThunk, deleteTaskThunk}