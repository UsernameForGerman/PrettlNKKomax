import API from "../api/api";
const AUTH_URL = "login/";
const LOGOUT_URL = "logout/"

class authApi extends API{
    constructor() {
        super(AUTH_URL);
    }

    auth = (login, password) => {
        return this.createObject({
            username : login,
            password : password
        }).then((resp) => {
            return resp.token;
        });
    }

    logout = () => {
        return this.createAPI().get(LOGOUT_URL);
    }
}

export default new authApi;