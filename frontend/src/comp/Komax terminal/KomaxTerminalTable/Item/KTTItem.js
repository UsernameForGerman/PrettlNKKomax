import classes from "./KTTItem.module.css"
import React from "react";
import IconButton from "../../../common/IconButton/IconButton";
let KomaxTerminalTableItem = (props) => {
    return(
        <div className={!props.heading ? classes.TableItem : classes.TableItemWithoutHover} onClick={props.select}>
            <div className={classes.firstItem}>
                {props.heading
                    ? <div className={classes.data}>
                        <b>{props.terminal_number[0]}</b>
                        <b>{props.terminal_number[1]}</b>
                    </div>
                    : <>{props.terminal_name}</>
                }
            </div>
            <div className={classes.firstItem}>
                {props.heading
                    ? <div className={classes.data}>
                        <b>{props.terminal_avaliable[0]}</b>
                        <b>{props.terminal_avaliable[1]}</b>
                    </div>
                    : <>{props.terminal_available ? "+" : "-"}</>
                }
            </div>
            <div className={classes.firstItem}>
                {props.heading
                    ? <div className={classes.data}>
                        <b>{props.material_avaliable[0]}</b>
                        <b>{props.material_avaliable[1]}</b>
                    </div>
                    : <>{props.seal_installed ? "+" : "-"}</>
                }
            </div>
            <div className={classes.firstItem}>
                {props.heading
                    ? <div className={classes.data}>
                        <b>{props.delete}</b>
                    </div>
                    : <IconButton icon={['fas', 'trash-alt']} click={props.del}/>
                }
            </div>
        </div>
    );
}

export default KomaxTerminalTableItem;