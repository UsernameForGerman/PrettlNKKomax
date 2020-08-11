import API  from "../api/api";

const BASE_URL = "harnesses/";

class harnessApi extends API{
    constructor() {
        super(BASE_URL);
    }

    getHarnessList = () => {
        return this.getObjectList();
    }

    getHarnessByNumber = (number) => {
        return this.getObjectById(number);
    }

    createHarness = (number, file) => {
        return this.createObject({
            harness_number : number,
            harness_chart : file
        }, this.createMediaAPI())
    }

    deleteHarnessByNumber = (number) => {
        return this.deleteObject(number, {
            number : number
        });
    }
}

export default new harnessApi;