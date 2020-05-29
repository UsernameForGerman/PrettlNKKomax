let createTerminal = (resp) => {
    return {
        terminal_number : resp.terminal_number,
        terminal_avaliable : resp.terminal_avaliable,
        material_avaliable : resp.material_avaliable
    }
}

export default createTerminal;