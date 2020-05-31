import authApi from "../DAL/auth/auth-api";

let checkLogged = () => {
    let token = window.localStorage.getItem('token');
    return !(token === null);
}

const initialState = {
    isFetching : false,
    isLogged : checkLogged(),
    errMsg : "",
    token : window.localStorage.getItem('token')
}

const TOGGLE_FETCHING = "LOGIN/TOGGLE_FETCHING";
const SET_LOGGED = "LOGIN/SET_LOGGED";
const SET_TOKEN = "LOGIN/SET_TOKEN";
const SET_ERROR = "LOGIN/ERROR";
const LOGOUT = "LOGIN/LOGOUT"

const loginReducer = (state = initialState, action) => {
    let stateCopy = {...state};
    switch (action.type) {
        case TOGGLE_FETCHING : {
            stateCopy.isFetching = !stateCopy.isFetching;
            break;
        }

        case SET_LOGGED : {
            stateCopy.isLogged = true;
            break;
        }

        case SET_TOKEN : {
            stateCopy.token = action.token;
            break;
        }

        case SET_ERROR : {
            stateCopy.errMsg = action.err;
            break;
        }

        case LOGOUT : {
            stateCopy.token = null;
            stateCopy.isLogged = false;
            stateCopy.errMsg = "";
            window.localStorage.clear();
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

const setLoggedAC = () => {
    return {
        type : SET_LOGGED
    }
}

const setTokenAC = (token) => {
    return {
        type : SET_TOKEN,
        token : token
    }
}

const setErrAC = (err) => {
    return {
        type : SET_ERROR,
        err : err
    }
}

const logoutAC = () => {
    return{
        type : LOGOUT
    }
}

const authThunk = (login, password) => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        authApi.auth(login, password).then((token) => {
            window.localStorage.setItem('token', token);
            dispatch(setTokenAC(token));
            dispatch(setLoggedAC());
            dispatch(toggleFetchAC());
        }).catch((err) => {
            dispatch(setErrAC("Invalid login or password"));
            dispatch(toggleFetchAC());
        });
    }
}

export {loginReducer, authThunk, logoutAC}