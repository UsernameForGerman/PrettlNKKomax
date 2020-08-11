import API from "../api/api";

const BASE_URL = "kappas/"

class kappa_api extends API{
    constructor() {
        super(BASE_URL);
    }

    getKappaList = () => {
        return this.getObjectList();
    }

    getKappaById = (id) => {
        return this.getObjectById(id);
    }

    createKappa = (number) => {
        return this.createObject({
            number : number
        });
    }

    updateKappa = (kappa) => {
        return this.updateObject(kappa.number, {...kappa});
    }
}

export default new kappa_api;