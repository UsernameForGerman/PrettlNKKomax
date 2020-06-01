import React from "react";
import {Redirect} from "react-router-dom";

let auth = (Component) => {
    return (props) => {
        let storage = window.localStorage;
        let token = storage.getItem('token');
        if (token !== null){
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