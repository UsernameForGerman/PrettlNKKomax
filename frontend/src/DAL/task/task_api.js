import API  from "../api/api";

const BASE_URL = "komax_tasks/";

class taskApi extends API{
    constructor() {
        super(BASE_URL);
    }

    getKomaxTasks = () => {
        return this.getObjectList();
    }
}

export default new taskApi;