import API from "../api/api";

const BASE_URL = "komax_terminals/"
class komax_terminal_api extends API {
    constructor() {
        super(BASE_URL);
    }

    getTerminalList = () => {
        return this.getObjectList();
    }

    createTerminal = (terminal) => {
        return this.createObject({

        });
    }

    updateTerminal = (terminal) => {
        return this.updateObject(terminal.number, {...terminal})
    }
}

export default new komax_terminal_api;