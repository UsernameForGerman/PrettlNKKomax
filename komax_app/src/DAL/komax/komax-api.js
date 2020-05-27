import {createAPI} from "../api/api";
import createKomax from "../models/komax";

const BASE_URL = "komaxes/"

let formIdUrl = (id) => {
    return BASE_URL + id;
}

class komaxApi {
    static getKomaxList = () => {
        return createAPI().get(BASE_URL).then((resp) => {
            let data = resp.data;
            data = data.map((elem) => {
                return createKomax(elem);
            });
            return data;
        });
    }

    static getKomaxById = (id) => {
        return createAPI().get(formIdUrl(id)).then((resp) => {
            let data = resp.data;
            return data;
        });
    }
}

export default komaxApi;