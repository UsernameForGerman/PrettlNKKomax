import classes from "./KomaxTable.module.css"
import React from "react";
import {getMarking, getSepairing, getStatus} from "../decrypter";

let KomaxTableItem = (props) => {
    let sepairing = props.sepairing;
    if (!props.columnType && props.sepairing){
        sepairing = props.sepairing.split(' ').map((elem) => {
            return <div key={elem}>{getSepairing(elem)}</div>
        });
    }
    let dataClasses = props.columnType ? classes.bold : classes.data;
    let tableItem = props.columnType ? classes.heading : classes.tableItem;
    let decrypt = (part, dechipher) => {
        return props.columnType !== "Heading" ? dechipher(part) : part
    }

    return(
      <div className={tableItem} onClick={props.click}>
        <div className={dataClasses} name={"number"}>
            {props.number}
        </div>
        <div className={dataClasses} name={"type"}>
            {props.type ? props.type : "Kappa"}
        </div>
        <div className={dataClasses} name={"status"}>
            {decrypt(props.status, getStatus)}
        </div>
        <div className={dataClasses} name={"marking"}>
            {decrypt(props.marking, getMarking)}
        </div>
        <div className={dataClasses} name={"pairing"}>
            {props.columnType !== "Heading" && props.type ? props.pairing ? "+" : "-" : props.pairing}
        </div>
        <div className={`${dataClasses} ${classes.sepairing}`} name={"separing"}>
            {sepairing}
        </div>
      </div>
    );
}

export default KomaxTableItem;