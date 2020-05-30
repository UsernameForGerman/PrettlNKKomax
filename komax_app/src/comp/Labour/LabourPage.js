import classes from "./LabourPage.module.css"
import React from "react";
let LabourPage = (props) => {
    return(
        <div className={classes.LabourPage}>
            <div className={classes.container}>
                <h1>
                    Laboriousness
                </h1>
                <div className={classes.table}>
                    <div className={classes.table_heading}>
                        <div className={classes.data}>
                            <b>Action</b>
                        </div>
                        <div className={classes.data}>
                            <b>Time (sec)</b>
                        </div>
                        <div className={classes.data}>
                            <button className={classes.create_btn}>
                                Create
                            </button>
                        </div>
                    </div>
                    {props.rows}
                </div>
            </div>
        </div>
    )
}

export default LabourPage;