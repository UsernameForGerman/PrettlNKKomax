import API  from "../api/api";

const BASE_URL = "komax_tasks/";

class task_api extends API{
    constructor() {
        super(BASE_URL);
    }

    getKomaxTasks = () => {
        return this.getObjectList();
    }

    createTask = (task) => {
        return this.createObject(task);
    }

    updateTask = (task) => {
        return this.updateObject(task.id, {...task});
    }
}

export default new task_api;