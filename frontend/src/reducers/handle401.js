import {logoutAC} from "./authReducer";

let handle401 = (err, dispatch) => {
    let status = err.response.status;
    if (status === 401){
        window.localStorage.clear();
        dispatch(logoutAC())
    }
}

export default handle401;

