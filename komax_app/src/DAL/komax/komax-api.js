import api from "../api/api";
import createKomax from "../models/komax";

const BASE_URL = "api/"

class komaxApi {
    static getKomaxList = () => {
        return api.get(BASE_URL).then((resp) => {
            let data = resp.data;
            data = data.map((elem) => {
                return createKomax(elem);
            });
            return data;
        });
    }
}

export default komaxApi;