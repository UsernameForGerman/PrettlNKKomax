import classes from "./KTTItem.module.css"
import React from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
let KomaxTerminalTableItem = (props) => {
    return(
        <div className={!props.heading ? classes.TableItem : classes.TableItemWithoutHover} onClick={props.select}>
            <div className={classes.firstItem}>
                {props.heading
                    ? <div className={classes.data}>
                        <b>{props.terminal_number[0]}</b>
                        <b>{props.terminal_number[1]}</b>
                    </div>
                    : <>{props.terminal_number}</>
                }
            </div>
            <div className={classes.firstItem}>
                {props.heading
                    ? <div className={classes.data}>
                        <b>{props.terminal_avaliable[0]}</b>
                        <b>{props.terminal_avaliable[1]}</b>
                    </div>
                    : <>{props.terminal_avaliable}</>
                }
            </div>
            <div className={classes.firstItem}>
                {props.heading
                    ? <div className={classes.data}>
                        <b>{props.material_avaliable[0]}</b>
                        <b>{props.material_avaliable[1]}</b>
                    </div>
                    : <>{props.material_avaliable}</>
                }
            </div>
            <div className={classes.firstItem}>
                {props.heading
                    ? <div className={classes.data}>
                        <b>{props.delete}</b>
                    </div>
                    : <button className={classes.deleteBtn}>
                        <FontAwesomeIcon icon={['fas', 'trash-alt']}/>
                      </button>
                }
            </div>
        </div>
    );
}

export default KomaxTerminalTableItem;