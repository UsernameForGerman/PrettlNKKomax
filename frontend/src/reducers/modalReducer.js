import komaxApi from "../DAL/komax/komax-api";
import handle401 from "./handle401";

let initialState = {
    isFetching : false,
    isValid : true,
    numberErrMsg : "",
    idErrMsg : ""
}

const TOGGLE_FETCHING = "MODAL/FETCHING";
const SET_VALID = "MODAL/SET_VALID";
const SET_NUMBER_ERR_MSG = "MODAL/NUMBER_MSG";
const SET_ID_ERR_MSG = "MODAL/ID_MSG";

let modalReducer = (state = initialState, action) => {
    let stateCopy = {...state};
    switch (action.type) {
        case TOGGLE_FETCHING : {
            stateCopy.isFetching = !stateCopy.isFetching;
            break;
        }
        case SET_VALID : {
            stateCopy.isValid = action.isValid;
            break;
        }
        case SET_ID_ERR_MSG : {
            stateCopy.idErrMsg = action.idErrMsg;
            break;
        }
        case SET_NUMBER_ERR_MSG : {
            stateCopy.numberErrMsg = action.numberErrMsg;
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

let setValidAC = (isValid) => {
    return {
        type : SET_VALID,
        isValid : isValid
    }
}

let setIdErrMsgAC = (errMsg) => {
    return {
        type : SET_ID_ERR_MSG,
        idErrMsg : errMsg
    }
}

let setNumberErrMsgAC = (errMsg) => {
    return {
        type : SET_NUMBER_ERR_MSG,
        numberErrMsg : errMsg
    }
}

let checkValidThunk = (number) => {
    return (dispatch) => {
        dispatch(toggleFetchingAC());
        komaxApi.getKomaxList()
            .then(data => {
               dispatch(toggleFetchingAC());
               let numberSet = data.map(elem => elem.number);
               if (numberSet.includes(number)){
                   dispatch(setNumberErrMsgAC("Komax с данным номером уже существует"));
                   dispatch(setIdErrMsgAC(""));
                   dispatch(setValidAC(false));
               } else if (number === 0){
                   dispatch(setNumberErrMsgAC("Заполните поле `Komax number`"));
                   dispatch(setIdErrMsgAC(""));
                   dispatch(setValidAC(false));
               } else {
                  dispatch(setValidAC(true));
                  dispatch(setIdErrMsgAC(""));
                  dispatch(setNumberErrMsgAC(""));
               }
            })
            .catch(err => {
                handle401(err, dispatch);
            });
    }
}

export {modalReducer, checkValidThunk}