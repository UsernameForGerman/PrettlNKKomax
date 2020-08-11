import classes from "./HCT.module.css"
import React from "react";
import HarnessesChooseTableItem from "./Item/HCTItem";
import {FormattedMessage} from "react-intl";
let HarnessesChooseTable = (props) => {
    let Heading = {
        harness_number : <FormattedMessage id={"harnesses.map_harnesses_number"}/>,
        created : <FormattedMessage id={"harnesses.table_date_label"}/>
    }
    return(
        <div className={classes.Table}>
            <HarnessesChooseTableItem {...Heading} role={props.role} heading/>
            {props.items}
        </div>
    )
}

export default HarnessesChooseTable;