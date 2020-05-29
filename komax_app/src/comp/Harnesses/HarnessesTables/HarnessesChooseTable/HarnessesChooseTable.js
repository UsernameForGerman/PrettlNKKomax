import classes from "./HCT.module.css"
import React from "react";
import HarnessesChooseTableItem from "./Item/HCTItem";
let HarnessesChooseTable = (props) => {
    let Heading = {
        harness_number : "Harnesses Number",
        created : "and\nDate"
    }
    return(
        <div className={classes.Table}>
            <HarnessesChooseTableItem {...Heading} heading/>
            {props.items}
        </div>
    )
}

export default HarnessesChooseTable;