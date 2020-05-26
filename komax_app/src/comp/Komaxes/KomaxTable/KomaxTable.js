import classes from "./KomaxTable.module.css"
import React from "react";
import KomaxTableItem from "./KomaxTableItem";
let KomaxTable = (props) => {
    let headings = {
        number : "Номер оборудования",
        type : "Тип",
        status : "Статус",
        marking : "Маркировка",
        pairing : "Спаривание",
        sepairing : "Группа сечения",
        id : "Идентификатор"
    };
    let renderedItems = props.items.map((elem) => {
        return (<KomaxTableItem {...elem} key={elem.number} click={() => {
            props.setSelected(elem);
            props.open();
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