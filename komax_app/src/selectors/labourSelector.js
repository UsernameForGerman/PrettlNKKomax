class LabourSelector {
    static getList = (state) => {
        return state.labour.labourList
    }

    static getFetching = (state) => {
        return state.labour.isFetching
    }
}

export default LabourSelector;