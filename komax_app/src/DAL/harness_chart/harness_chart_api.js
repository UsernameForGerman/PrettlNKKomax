import API from "../api/api";
const BASE_URL = "http://localhost:8000/api/v1/";
const HARNESSES_BASE_URL = "harness_chart/";

class harnessChartApi extends API {
    constructor() {
        super(HARNESSES_BASE_URL);
    }

    getHarnessChartByNumber = (number) => {
        return this.createAPI(BASE_URL).get(BASE_URL + HARNESSES_BASE_URL + number).then(resp => {
            return resp.data;
        })
    }
}

export default new harnessChartApi;