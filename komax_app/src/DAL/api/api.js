import axios from "axios";

const BASE_URL = "http://localhost:8000/api/v2/";

class API {
    constructor(base_url) {
        this.base_url = BASE_URL + base_url;
    }

    getToken = () => {
        let token = window.localStorage.getItem('token');
        if (!token){
            token = "null";
        }
        return token;
    }

    createAPI = (baseUrl = BASE_URL) => {
        let token = this.getToken();
        return axios.create({
            baseURL : baseUrl,
            headers : {
                "Authorization": `Token ${token}`,
                "Content-Type" : "application/json",
            }
        });
    }

    createMediaAPI = () => {
        let token = this.getToken();
        return axios.create({
            baseURL : BASE_URL,
            headers : {
                "Authorization": `Token ${token}`,
                "Content-Type" : "multipart/form-data",
            }
        });
    }

    formIdUrl = (id) => {
        return this.base_url + id;
    }

    getObjectList = () => {
        return this.createAPI().get(this.base_url).then((resp) => {
            let data = resp.data;
            return data;
        });
    }

    getObjectById = (id) => {
        return this.createAPI().get(this.formIdUrl(id)).then((resp) => {
            return resp.data;
        });
    }

    createObject = (options) => {
        return this.createAPI().post(this.base_url, options).then((resp) => {
            return resp.data;
        });
    }

    deleteObject = (id, options) => {
        return this.createAPI().delete(this.formIdUrl(id), options).then((resp) => {
            return resp.data;
        });
    }

    updateObject = (id, options) => {
        return this.createAPI().put(this.formIdUrl(id), options).then(resp => {
            return resp;
        })
    }
}

export default API;