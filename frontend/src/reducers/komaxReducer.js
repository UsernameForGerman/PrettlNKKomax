import komaxApi from "../DAL/komax/komax-api";

const initialState = {
    isFetching : false,
    komaxList : [],
    statuses : []
}

const TOGGLE_FETCHING = "KOMAX/TOGGLE_FETCHING";
const SET_LIST = "KOMAX/TOGGLE_SET_LIST";
const SET_STATUSES = "KOMAX/STATUSES";

const komaxReducer = (state = initialState, action) => {
    let stateCopy = {...state};
    switch (action.type) {
        case TOGGLE_FETCHING : {
            stateCopy.isFetching = !stateCopy.isFetching;
            break;
        }

        case SET_LIST : {
            stateCopy.komaxList = action.list.sort((elem, elem2) => {
                return elem.number - elem2.number
            });
            break;
        }

        case SET_STATUSES : {
            stateCopy.statuses = action.statuses
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

const setStatusesAC = (statuses) => {
    return {
        type : SET_STATUSES,
        statuses : statuses
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

const getStatusesThunk = () => {
    return (dispatch) => {
        let send = () => {
            komaxApi.getStatuses()
                .then(resp => {
                    let path = window.location.pathname;
                    if (path === "/komaxes"){
                        dispatch(setStatusesAC(resp));
                        setTimeout(() => {
                            send();
                        }, 2000);
                    } else {
                        return '';
                    }
                })
                .catch(err => {
                    console.log(err);
                })
        }
        send();
    }
}

export {toggleFetchAC, setListAC, komaxReducer, getListThunk, createKomaxThunk, updateKomaxThunk, getStatusesThunk};