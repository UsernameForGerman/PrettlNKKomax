import React from "react";
import classes from "./LandingPage.module.css";
import LandingHeading from "./LandingHeading/LandingHeading";
import DescSection from "./DescSection/DescSection";
import Infographics from "./Infographics/Infographics";
let LandingPage = (props) => {
    return (
        <div className={classes.container}>
            <LandingHeading/>
            <DescSection/>
            <Infographics/>
        </div>
    )
}

export default LandingPage;