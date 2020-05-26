import classes from "./HCTItem.module.css"
import React from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
let HarnessesChooseTableItem = (props) => {
    return(
        <div className={!props.heading ? classes.TableItem : classes.TableItemWithoutHover}>
            <div className={classes.firstItem}>
                <div className={classes.data}>
                    {props.heading
                        ? <b>{props.number}</b>
                        : <>{props.number}</>
                    }
                </div>
                <div className={classes.data}>
                    {props.heading
                        ? <b>{props.date}</b>
                        : <>{props.date}</>
                    }
                </div>
            </div>
            {!props.heading
                ?<div className={classes.toolbar}>
                    <button className={`${classes.iconButton} ${classes.downloadBtn}`}>
                        <FontAwesomeIcon icon={['fas', 'download']}/>
                    </button>
                    <button className={`${classes.iconButton} ${classes.deleteBtn}`}>
                        <FontAwesomeIcon icon={['fas', 'trash-alt']}/>
                    </button>
                 </div>
                :<>
                    <div className={`${classes.firstItem} ${classes.secondItem}`}>
                        <div className={classes.data}>
                            <b>Download</b>
                        </div>
                        <div className={classes.data}>
                            <b>Delete</b>
                        </div>
                    </div>
                </>
            }
        </div>
    );
}

export default HarnessesChooseTableItem;