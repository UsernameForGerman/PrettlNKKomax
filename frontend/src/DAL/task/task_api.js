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

    loadTask = (task) => {
        return this.createAPI().put("load_komax_task/",{
            task_name : task.name
        }).then(resp => resp.data);
    }

    sendTask = (task) => {
        return this.createAPI().put("send_komax_task/", {
            task_name : task.name
        }).then(resp => resp.data);
    }

    deleteTask = (task) => {
        return this.createAPI().delete(BASE_URL + task.name + "");
    }
}

export default new task_api;