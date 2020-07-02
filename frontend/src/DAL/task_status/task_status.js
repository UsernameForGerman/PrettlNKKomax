import api from "../api/api";
const BASE_URL = "komax_task_status/"
class Task_status_api extends api{
    constructor() {
        super(BASE_URL);
    }

    getStatuses = () => {
        return this.getObjectList();
    }
}

export default new Task_status_api();

