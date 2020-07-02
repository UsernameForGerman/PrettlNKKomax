class KomaxSelector {
    static getList = (state) => {
        return state.komaxes.komaxList
    }

    static getFetching = (state) => {
        return state.komaxes.isFetching
    }

    static getStatuses = (state) => {
        return state.komaxes.statuses
    }
}

export default KomaxSelector;