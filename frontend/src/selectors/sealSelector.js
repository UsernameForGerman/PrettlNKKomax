class SealSelector {
    static getFetching = (state) => {
        return state.seal.isFetching;
    }

    static getList = (state) => {
        return state.seal.sealsList;
    }
}

export default SealSelector;