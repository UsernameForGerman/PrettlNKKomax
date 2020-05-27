import {createAPI} from "../api/api";

const BASE_URL = "auth/"

class authApi {
    static auth = (login, password) => {
        return createAPI().post(BASE_URL, {
            username : login,
            password : password
        }).then((resp) => {
            return resp.data.token;
        });
    }
}

export default authApi;