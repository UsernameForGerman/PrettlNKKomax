class TasksSelector {
    static getList = (state) => {
        return state.tasks.tasksList
    }

    static getFetching = (state) => {
        return state.tasks.isFetching
    }

    static getErrMsg = (state) => {
        return state.tasks.errMsg
    }

    static getValid = (state) => {
        return state.tasks.isValid
    }

    static getCanSend = (state) => {
        return state.tasks.canSend
    }
}

export default TasksSelector;