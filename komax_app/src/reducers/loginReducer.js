import authApi from "../DAL/auth/auth-api";

const initialState = {
    isFetching : false,
    isLogged : false,
    token : ""
}

const TOGGLE_FETCHING = "LOGIN/TOGGLE_FETCHING";
const SET_LOGGED = "LOGIN/SET_LOGGED";
const SET_TOKEN = "LOGIN/SET_TOKKEN";

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

const authThunk = (login, password) => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        authApi.auth(login, password).then((token) => {
            dispatch(setLoggedAC());
            dispatch(setTokenAC(token));
            window.localStorage.setItem('token', token);
            dispatch(toggleFetchAC());
        });
    }
}

export {loginReducer, authThunk}