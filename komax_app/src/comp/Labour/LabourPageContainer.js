import LabourPage from "./LabourPage";
import React from "react";
import auth from "../AuthHOC/authHOC";
import classes from "./LabourPage.module.css"

let LabourPageContainer = (props) => {
    let items = [
        {
            action : "a",
            time : "123"
        },
        {
            action : "b",
            time : "12213"
        },
        {
            action : "c",
            time : "7565"
        },
        {
            action : "d",
            time : "321"
        },
        {
            action : "e",
            time : "965467"
        },
        {
            action : "f",
            time : "4654745"
        }
    ].map(elem => {
        return(
            <div className={classes.data_row}>
                <div className={classes.data}>
                    {elem.action}
                </div>
                <div className={classes.data}>
                    {elem.time}
                </div>
                <div className={classes.data}>
                    <button className={classes.edit_btn}>
                        Edit
                    </button>
                </div>
            </div>
        )
    })
    return(
        <LabourPage rows={items}/>
    )
}

export default auth(LabourPageContainer);