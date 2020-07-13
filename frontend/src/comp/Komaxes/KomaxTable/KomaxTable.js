import classes from "./KomaxTable.module.css"
import React from "react";
import KomaxTableItem from "./KomaxTableItem";
import {FormattedMessage} from "react-intl";
let KomaxTable = (props) => {
    let headings = {
        number : <FormattedMessage id={"komax.number_label"}/>,
        type : <FormattedMessage id={"komax.type_label"}/>,
        status : <FormattedMessage id={"komax.status_label"}/>,
        marking : <FormattedMessage id={"komax.marking_label"}/>,
        pairing : <FormattedMessage id={"komax.pairing_label"}/>,
        sepairing : <FormattedMessage id={"komax.group_of_square_label"}/>,
        id : <FormattedMessage id={"komax.identifier_label"}/>,
    };
    let renderedItems = props.items.map((elem) => {
        return (<KomaxTableItem {...elem} key={elem.number} click={() => {
            if (elem.type){
                props.setSelected(elem);
                props.open();
            }
        }}/>);
    });
    return(
        <div className={classes.Table}>
            <KomaxTableItem {...headings} columnType={"Heading"}/>
            {renderedItems}
        </div>
    );
}

export default KomaxTable;