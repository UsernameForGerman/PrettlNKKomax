import classes from "./Table.module.css"
import React from "react";
import TableItem from "./TableItem";
let Table = (props) => {
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
        return (<TableItem {...elem} click={() => {
            props.setSelected(elem);
            props.open();
        }}/>);
    });
    return(
        <div className={classes.Table}>
            <TableItem {...headings} columnType={"Heading"}/>
            {renderedItems}
        </div>
    );
}

export default Table;