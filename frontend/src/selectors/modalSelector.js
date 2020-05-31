class ModalSelector {
    static getNumberErrMsg = (state) => {
        return state.modal.numberErrMsg
    }

    static getIdErrMsg = (state) => {
        return state.modal.idErrMsg
    }

    static getFetching = (state) => {
        return state.modal.isFetching
    }

    static getValid = (state) => {
        return state.modal.isValid
    }
}

export default ModalSelector;