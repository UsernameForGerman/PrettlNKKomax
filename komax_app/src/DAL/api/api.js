import axios from "axios";
const BASE_URL = "http://localhost:8000/api/v1/";
const api = axios.create({
    baseURL : BASE_URL,
    headers : {
        "Content-Type" : "application/json",
    }
});

const getToken = () => {
    let token = window.localStorage.getItem('token');
    if (!token){
        token = "null";
    }
    return token;
}

const createAPI = () => {
    let token = getToken();
    return axios.create({
        baseURL : BASE_URL,
        headers : {
            "Authorization": `Token ${token}`,
            "Content-Type" : "application/json",
        }
    });
}

const createMediaAPI = () => {
    let token = getToken();
    return axios.create({
        baseURL : BASE_URL,
        headers : {
            "Authorization": `Token ${token}`,
            "Content-Type" : "multipart/form-data",
        }
    });
}

export {createAPI, createMediaAPI};