import {logoutThunk} from "./authReducer";

let handle401 = (err, dispatch) => {
    if (err.status === 401) dispatch(logoutThunk());
}

export default handle401;

