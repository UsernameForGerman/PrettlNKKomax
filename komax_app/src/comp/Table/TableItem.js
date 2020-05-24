import classes from "./Table.module.css"
import React from "react";

let TableItem = (props) => {
    let separing = props.sepairing.split(' ').map((elem) => {
        return <div>{elem}</div>
    });
    let dataClasses = props.columnType ? classes.bold : classes.data;
    let tableItem = props.columnType ? classes.heading : classes.tableItem;
    return(
      <div className={tableItem} onClick={props.click}>
        <div className={dataClasses} name={"number"}>
            {props.number}
        </div>
        <div className={dataClasses} name={"type"}>
            {props.type}
        </div>
        <div className={dataClasses} name={"status"}>
            {props.status}
        </div>
        <div className={dataClasses} name={"marking"}>
            {props.marking}
        </div>
        <div className={dataClasses} name={"pairing"}>
            {props.pairing}
        </div>
        <div className={`${dataClasses} ${classes.sepairing}`} name={"separing"}>
            {separing}
        </div>
        <div className={dataClasses} name={"id"}>
            {props.id}
        </div>
      </div>
    );
}

export default TableItem;