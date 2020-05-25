class KomaxSelector {
    static getList = (state) => {
        return state.komaxes.komaxList
    }

    static getFetching = (state) => {
        return state.komaxes.isFetching
    }
}

export default KomaxSelector;