class HarnessSelector {
    static getList = (state) => {
        return state.harnesses.harnessesList
    }

    static getFetching = (state) => {
        return state.harnesses.isFetching
    }

    static getMap = (state) => {
        return state.harnesses.selectedMap
    }
}

export default HarnessSelector;