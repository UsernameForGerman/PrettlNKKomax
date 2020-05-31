class TerminalSelector {
    static getList = (state) => {
        return state.terminals.terminalsList
    }

    static getFetching = (state) => {
        return state.terminals.isFetching
    }
}

export default TerminalSelector;