class LoginSelector {
    static getToken = (state) => {
        return state.login.token
    }

    static getFetching = (state) => {
        return state.login.isFetching
    }

    static getLogged = (state) => {
        return state.login.isLogged
    }

    static getErr = (state) => {
        return state.login.errMsg;
    }
}

export default LoginSelector;