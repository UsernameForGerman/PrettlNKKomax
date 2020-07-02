import API from "../api/api";
const BASE_URL = "groups/"
class Group_api extends API{
    constructor() {
        super(BASE_URL);
    }

    getGroup = () => {
        return this.getObjectList();
    }
}

export default new Group_api();