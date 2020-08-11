class KappaSelector {
    static getList = (state) => {
        return state.kappa.kappasList
    }

    static getFetching = (state) => {
        return state.kappa.isFetching
    }
}

export default KappaSelector;