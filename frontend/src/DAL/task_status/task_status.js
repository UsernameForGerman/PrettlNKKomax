import api from "../api/api";
const BASE_URL = "/komax_task_status/"
class Task_status extends api{
    constructor() {
        super(BASE_URL);
    }

    getStatuses = () => {
        return
    }
}