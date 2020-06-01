import API from "../api/api";
const BASE_URL = "harness_chart/";

class harnessChartApi extends API {
    constructor() {
        super(BASE_URL);
    }

    getHarnessChartByNumber = (number) => {
        return this.getObjectById(number);
    }
}

export default new harnessChartApi;