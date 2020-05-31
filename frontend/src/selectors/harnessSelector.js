class HarnessSelector {
    static getList = (state) => {
        return state.harnesses.harnessesList
    }

    static getFetching = (state) => {
        return state.harnesses.isFetching
    }

    static getMapFetching = (state) => {
        return state.harnesses.isMapFetching
    }

    static getMap = (state) => {
        return state.harnesses.selectedMap
    }
}

export default HarnessSelector;