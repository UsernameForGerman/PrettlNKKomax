import API  from "../api/api";

const BASE_URL = "tasks/";

class taskApi extends API{
    constructor() {
        super(BASE_URL);
    }

}

export default new taskApi;