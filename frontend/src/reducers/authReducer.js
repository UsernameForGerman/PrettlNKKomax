import authApi from "../DAL/auth/auth-api";
import group_api from "../DAL/group_api/group_api";
import choose_komax_api from "../DAL/choose_komax/choose_komax_api";

let checkLogged = () => {
    let token = window.localStorage.getItem('token');
    return !(token === null);
}

let get = (prop) => {
    let value = window.localStorage.getItem(prop);
    if (value === null) return "";
    return value;
}

const initialState = {
    isFetching : false,
    isLogged : checkLogged(),
    errMsg : "",
    token : get('token'),
    login : get('login'),
    role : get('role'),
    komax : get('komax')
}

const TOGGLE_FETCHING = "LOGIN/TOGGLE_FETCHING";
const SET_LOGGED = "LOGIN/SET_LOGGED";
const SET_TOKEN = "LOGIN/SET_TOKEN";
const SET_ERROR = "LOGIN/ERROR";
const SET_LOGIN = "LOGIN/SET_LOGIN";
const SET_ROLE = "LOGIN/SET_ROLE";
const SET_KOMAX = "LOGIN/SET_KOMAX";
const LOGOUT = "LOGIN/LOGOUT";

const authReducer = (state = initialState, action) => {
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

        case SET_LOGIN : {
            stateCopy.login = action.login;
            break;
        }

        case SET_ROLE : {
            stateCopy.role = action.role;
            break;
        }

        case LOGOUT : {
            stateCopy.token = null;
            stateCopy.isLogged = false;
            stateCopy.errMsg = "";
            stateCopy.login = "";
            stateCopy.role = "";
            stateCopy.komax = "";
            window.localStorage.clear();
            break;
        }

        case SET_KOMAX : {
            stateCopy.komax = action.komax;
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

const setLoginAC = (login) => {
    return {
        type : SET_LOGIN,
        login : login
    }
}

const setRoleAC = (role) => {
    return {
        type : SET_ROLE,
        role : role
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

const setKomaxAC = (komax) => {
    return {
        type : SET_KOMAX,
        komax : komax
    }
}


const authThunk = (login, password) => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        authApi.auth(login, password).then((token) => {
            window.localStorage.setItem('token', token);
            dispatch(setTokenAC(token));
            dispatch(setLoginAC(login));
            window.localStorage.setItem('login', login);
            dispatch(setLoggedAC());
            group_api.getGroup().then(data => {
                if (data.length === 0) return 'Admin';
                return data[0].name
            }).then(role => {
                dispatch(setRoleAC(role));
                window.localStorage.setItem('role', role);
                dispatch(toggleFetchAC());
            });
        }).catch((err) => {
            dispatch(setErrAC("Invalid login or password"));
            dispatch(toggleFetchAC());
        });
    }
}

const logoutThunk = () => {
    return (dispatch) => {
        dispatch(toggleFetchAC());
        authApi.logout().then(resp => {
            dispatch(logoutAC());
            dispatch(toggleFetchAC());
        })
    }
}

const chooseKomaxThunk = (login, number) => {
    return (dispatch) => {
        window.localStorage.setItem('komax', number);
        choose_komax_api.chooseKomax(login, number).then(resp => {
            dispatch(setKomaxAC(number));
        });
    }
}

export {authReducer, authThunk, logoutThunk, chooseKomaxThunk, logoutAC}