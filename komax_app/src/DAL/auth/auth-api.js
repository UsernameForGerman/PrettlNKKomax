import API from "../api/api";

const BASE_URL = "http://localhost:8000/api/v1/";
const AUTH_URL = "auth/";

class authApi extends API{
    constructor() {
        super(AUTH_URL);
    }

    auth = (login, password) => {
        return this.createAPI(BASE_URL).post(BASE_URL + AUTH_URL, {
            username : login,
            password : password
        }).then((resp) => {
            return resp.data.token;
        });
    }
}

export default new authApi;