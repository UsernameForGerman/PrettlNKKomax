import React from "react";
import img from "../../../assets/images/Preloader.gif"
import classes from "./Preloader.module.css"

let Preloader = (props) => {
    return(
        <div className={classes.Preloader}>
            <img src={img} alt={"Preloader"} className={classes.img}/>
        </div>
    );
}

export default Preloader;