import SuccessButton from "../../common/SuccessButton/SuccessButton";
import React from "react";
import classes from "./LandingHeading.module.css";

let handleClick = () => {
    window.location.href = "login";
}
let LandingHeading = (props) => {
    return (
        <header className={classes.header}>
            <div className={classes.tetra_heading}>
                TetraD-NK
            </div>
            <div className={classes.prettl_heading}>
                <div className={classes.prettl}>Prettl-NK</div>
                <SuccessButton value={"Login"} class={classes.login_btn} click={handleClick}/>
            </div>
        </header>
    )
}

export default LandingHeading;