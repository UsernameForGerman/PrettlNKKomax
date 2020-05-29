import API from "../api/api";

const BASE_URL = "auth/"

class authApi extends API{
    constructor() {
        super(BASE_URL);
    }

    auth = (login, password) => {
        return this.createAPI().post(BASE_URL, {
            username : login,
            password : password
        }).then((resp) => {
            return resp.data.token;
        });
    }
}

export default new authApi;