import React from "react";
import classes from "./LandingPage.module.css";
import LandingHeading from "./LandingHeading/LandingHeading";
import DescSection from "./DescSection/DescSection";
let LandingPage = (props) => {
    return (
        <div className={classes.container}>
            <LandingHeading/>
            <DescSection/>
        </div>
    )
}

export default LandingPage;