import React from "react";
import classes from "./Stages.module.css";
import stages from "../../../assets/images/stages.png";

let Stages = (props) => {
    return (
        <section className={classes.stages}>
            <div className={classes.heading}>
                Внедренные процессы в производство и поставку
            </div>
            <img src={stages} className={classes.img} alt={"Stages"}/>
        </section>
    )
}

export default Stages;