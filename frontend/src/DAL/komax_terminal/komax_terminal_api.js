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
            terminal_name : terminal.terminal_name
        });
    }

    updateTerminal = (terminal) => {
        return this.updateObject(terminal.terminal_name, {...terminal})
    }

    deleteTerminal = (terminal) => {
        return this.deleteObject(terminal.terminal_name);
    }
}

export default new komax_terminal_api;