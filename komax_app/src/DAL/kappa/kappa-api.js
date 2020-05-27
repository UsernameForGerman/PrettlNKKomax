import {createAPI} from "../api/api";
import createKomax from "../models/komax";

const BASE_URL = "kappas/"

let formIdUrl = (id) => {
  return BASE_URL + id;
}

class kappaApi {
    static getKappaList = () => {
        return createAPI().get(BASE_URL).then((resp) => {
            let data = resp.data;
            return data;
        });
    }

    static getKappaById = (id) => {
        return createAPI().get(formIdUrl(id)).then((resp) => {
            let data = resp.data;
            return data;
        });
    }

    static createKappa = (number) => {
        return createAPI().post(BASE_URL, {
            number : number
        }).then((resp) => {
            let data = resp.data;
            return data;
        });
    }

    static options = () => {
        return createAPI().head(BASE_URL);
    }
}

export default kappaApi;