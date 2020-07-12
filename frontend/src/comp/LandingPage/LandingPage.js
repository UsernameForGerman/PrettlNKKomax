import React from "react";
import classes from "./LandingPage.module.css";
import LandingHeading from "./LandingHeading/LandingHeading";
import DescSection from "./DescSection/DescSection";
import Infographics from "./Infographics/Infographics";
import Stages from "./Stages/Stages";
import Feedback from "./Feedback/Feedback";
let LandingPage = (props) => {
    return (
        <div className={classes.container}>
            <LandingHeading/>
            <DescSection/>
            <Infographics/>
            <Stages/>
            <Feedback/>
        </div>
    )
}

export default LandingPage;