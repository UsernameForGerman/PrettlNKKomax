import API from "../api/api";
const BASE_URL = "workers/"
class Choose_komax_api extends API{
    constructor() {
        super(BASE_URL);
    }

    chooseKomax = (username, komax) => {
        return this.createAPI().put(BASE_URL + username + "/", {
            current_komax : komax
        })
    }
}

export default new Choose_komax_api();