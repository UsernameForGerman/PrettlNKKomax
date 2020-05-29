import classes from "./KomaxTerminalTable.module.css"
import React from "react";
import KomaxTerminalTableItem from "./Item/KTTItem";
let KomaxTerminalTable = (props) => {
    let Heading = {
        terminal_number : ["Terminal", "number"],
        terminal_avaliable : ["Terminal", "avaliable"],
        material_avaliable : ["Material", "avaliable"],
        delete : "Delete"
    }
    return(
        <div className={classes.Table}>
            <KomaxTerminalTableItem {...Heading} heading/>
            {props.items}
        </div>
    )
}

export default KomaxTerminalTable;