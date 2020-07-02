import API from "../api/api";
const BASE_URL = "laboriousness/"
class labourApi extends API{
    constructor() {
        super(BASE_URL);
    }

    getLabourList = () => {
        return this.getObjectList();
    }

    createLabour = (labour) => {
        return this.createObject({...labour})
    }

    updateLabour = (labour) => {
        return this.updateObject(labour.action, {...labour});
    }
}

export default new labourApi;