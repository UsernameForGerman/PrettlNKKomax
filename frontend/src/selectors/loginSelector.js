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

    static getLogin = (state) => {
        return state.login.login;
    }

    static getRole = (state) => {
        return state.login.role;
    }

    static getErr = (state) => {
        return state.login.errMsg;
    }

    static getKomax = (state) => {
        return state.login.komax;
    }
}

export default LoginSelector;