import React from "react";
import {Redirect} from "react-router-dom";
import get_pages from "./get_pages"
let auth = (Component) => {
    return (props) => {
        let storage = window.localStorage;
        let pathname = window.location.pathname;
        let index = pathname.toString().substr(1).indexOf('/');
        let path = window.location.pathname.toString().substr(1, index > 0 ? index : pathname.length);
        let token = storage.getItem('token');
        let role = storage.getItem('role');
        let availPages = get_pages(role);
        if (token !== null && (path === 'account' || path === '' || availPages.includes(path))){
            return(
                <Component {...props}/>
            );
        } else {
            return (
                <Redirect to={"/login"}/>
            )
        }
    }
}

export default auth;