import React from "react";
import {Redirect} from "react-router-dom";

let auth = (Component) => {
    return (props) => {
        let storage = window.localStorage;
        let token = storage.getItem('token');
        if (token){
            return(
                <Component {...props}/>
            );
        } else {
            return (
                <Redirect to={"/"}/>
            )
        }
    }
}

export default auth;