import API from "../api/api";

const BASE_URL = "komax_seals/"
class komax_seal_api extends API {
    constructor() {
        super(BASE_URL);
    }

    getSealsList = () => {
        return this.getObjectList();
    }
}

export default new komax_seal_api;