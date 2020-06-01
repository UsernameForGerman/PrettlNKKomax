import API from "../api/api";
const AUTH_URL = "login/";

class authApi extends API{
    constructor() {
        super(AUTH_URL);
    }

    auth = (login, password) => {
        return this.createObject({
            username : login,
            password : password
        }).then((resp) => {
            return resp.data.token;
        });
    }
}

export default new authApi;