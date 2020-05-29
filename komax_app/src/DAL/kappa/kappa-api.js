import API from "../api/api";

const BASE_URL = "kappas/"

class kappaApi extends API{
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
}

export default new kappaApi;