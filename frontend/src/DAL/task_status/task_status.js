import api from "../api/api";
const BASE_URL = "komax_task_status/"
class Task_status_api extends api{
    constructor() {
        super(BASE_URL);
    }

    getStatuses = (name) => {
<<<<<<< HEAD
        return this.getObjectList("?task-name=" + name + "");
=======
        return this.getObjectList("?task-name=" + name);
>>>>>>> 187ac9fd0074931a9d05a3e0d4ac61a9031a29de
    }
}

export default new Task_status_api();

