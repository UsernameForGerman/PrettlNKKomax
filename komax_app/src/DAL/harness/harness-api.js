import {createAPI, createMediaAPI} from "../api/api";

const BASE_URL = "harnesses/";

let formIdUrl = (id) => {
  return BASE_URL + id;
}

class harnessApi {
    static getHarnessList = () => {
        return createAPI().get(BASE_URL).then((resp) => {
            let data = resp.data;
            return data;
        });
    }

    static getHarnessByNumber = (number) => {
        return createAPI().get(formIdUrl(number)).then((resp) => {
            let data = resp.data;
            return data;
        });
    }

    static createHarness = (number, file) => {
        return createMediaAPI().post(BASE_URL, {
            number : number,
            data : file
        }).then((resp) => {
            let data = resp.data;
            return data;
        });
    }

    static options = () => {
        return createAPI().head(BASE_URL);
    }
}

export default harnessApi;