import axios from "axios";
import BASE_URL from "../getBaseUrl";

const API_URL = BASE_URL + "api/v1/";

class API {
    constructor(base_url) {
        this.base_url = API_URL + base_url;
    }

    getToken = () => {
        let token = window.localStorage.getItem('token');
        if (!token){
            token = "null";
        }
        return token;
    }

    createAPI = (baseUrl = API_URL) => {
        let token = this.getToken();
        if (token === "null"){
            return axios.create({
                baseURL : baseUrl,
                headers : {
                    "Content-Type" : "application/json"
                }
            });
        } else {
           return axios.create({
                baseURL : baseUrl,
                headers : {
                    "Authorization": `Token ${token}`,
                    "Content-Type" : "application/json",
                }
            });
        }
    }

    createMediaAPI = () => {
        let token = this.getToken();
        if (token === "null"){
            return axios.create({
                baseURL : API_URL,
                headers : {
                    "Content-Type" : "multipart/form-data"
                }
            });
        } else {
           return axios.create({
                baseURL : API_URL,
                headers : {
                    "Authorization": `Token ${token}`,
                    "Content-Type" : "multipart/form-data",
                }
            });
        }
    }

    formIdUrl = (id) => {
        return this.base_url + id;
    }

    getObjectList = (params="") => {
        return this.createAPI().get(this.base_url + params).then((resp) => {
            let data = resp.data;
            return data;
        });
    }

    getObjectById = (id, url = this.formIdUrl(id)) => {
        return this.createAPI().get(this.formIdUrl(id)).then((resp) => {
            return resp.data;
        });
    }

    createObject = (options, url = "", api = this.createAPI()) => {
        return api.post(this.base_url + url, options).then((resp) => {
            return resp.data;
        });
    }

    deleteObject = (id, options) => {
        return this.createAPI().delete(this.formIdUrl(id), options).then((resp) => {
            return resp.data;
        });
    }

    updateObject = (id, options) => {
        return this.createAPI().put(this.formIdUrl(id) + "/", options).then(resp => {
            return resp;
        })
    }
}

export default API;