import API from "../api/api";

const BASE_URL = "komax_seals/"
class komax_seal_api extends API {
    constructor() {
        super(BASE_URL);
    }

    getSealsList = () => {
        return this.getObjectList();
    }

    getSealByID = (id) => {
        return this.getObjectById(id);
    }

    updateSeal = (seal) => {
        return this.updateObject(seal.seal_name, {...seal});
    }

    createSeal = (seal) => {
        return this.createObject({...seal});
    }

    deleteSeal = (seal) => {
        return this.deleteObject(seal.seal_name, {...seal});
    }
}

export default new komax_seal_api;