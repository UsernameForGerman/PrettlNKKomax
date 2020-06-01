let createKomax = (response) => {
    return {
        number : response.number,
        type : "Komax",
        status : response.status,
        marking : response.marking,
        pairing : response.pairing,
        sepairing : response.group_of_square,
        id : response.identifier
    }
}

export default createKomax;