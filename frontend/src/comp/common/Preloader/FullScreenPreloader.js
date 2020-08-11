import Preloader from "./Preloader";
import classes from "./Preloader.module.css"
import React from "react";

let FullScreenPreloader = (props) => {
    return (
        <div className={classes.wrapper}>
            <Preloader/>
        </div>
    )
}

export default FullScreenPreloader;