import classes from "./KomaxTerminalTable.module.css"
import React from "react";
import KomaxTerminalTableItem from "./Item/KTTItem";
import {FormattedMessage} from "react-intl";
let KomaxTerminalTable = (props) => {
    let Heading = {
        terminal_number : [<FormattedMessage id={"terminal.terminal_number_0_label"}/>, <FormattedMessage id={"terminal.terminal_number_1_label"}/>],
        terminal_avaliable : [<FormattedMessage id={"terminal.terminal_avaliable_0_label"}/>, <FormattedMessage id={"terminal.terminal_avaliable_1_label"}/>],
        material_avaliable : [<FormattedMessage id={"terminal.material_avaliable_0_label"}/>, <FormattedMessage id={"terminal.material_avaliable_1_label"}/>],
        delete : <FormattedMessage id={"terminal.delete_label"}/>
    }

    return(
        <div className={classes.Table}>
            <KomaxTerminalTableItem {...Heading} heading/>
            {props.items}
        </div>
    )
}

export default KomaxTerminalTable;