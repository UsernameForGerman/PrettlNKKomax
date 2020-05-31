import API from "../api/api";
import createKomax from "../models/komax";

const BASE_URL = "komaxes/"

class komaxApi extends API {
    constructor() {
        super(BASE_URL);
    }

    getKomaxList = () => {
        return this.createAPI().get(BASE_URL).then((resp) => {
            let data = resp.data;
            data = data.map((elem) => {
                return createKomax(elem);
            });
            return data;
        });
    }

    getKomaxById = (id) => {
        return this.getObjectById(id);
    }

    createKomax = (komax) => {
        return this.createObject({...komax});
    }

    updateKomax = (komax) => {
        return this.updateObject(komax.number, {...komax});
    }
}

export default new komaxApi;