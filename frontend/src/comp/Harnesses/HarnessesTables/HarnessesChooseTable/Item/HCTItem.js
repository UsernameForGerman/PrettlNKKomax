import classes from "./HCTItem.module.css"
import React from "react";
import IconButton from "../../../../common/IconButton/IconButton";
import {FormattedMessage} from "react-intl";
const BASE_URL = "http://localhost:8000/"
let HarnessesChooseTableItem = (props) => {
    return(
        <div className={!props.heading ? classes.TableItem : classes.TableItemWithoutHover} onClick={props.select}>
            <div className={classes.firstItem}>
                <div className={classes.data}>
                    {props.heading
                        ? <b>{props.harness_number}</b>
                        : <>{props.harness_number}</>
                    }
                </div>
                <div className={classes.data}>
                    {props.heading
                        ? <b>{props.created}</b>
                        : <>{props.created}</>
                    }
                </div>
            </div>
            {!props.heading
                ? props.role.toLowerCase() !== "master" ? <div className={classes.toolbar}>
                    <a href={BASE_URL + "harnesses/" + props.harness_number +"/download/"} target={"blank"}>
                        <IconButton icon={['fas', 'download']}/>
                    </a>
                    <IconButton icon={['fas', 'trash-alt']} click={props.delete}/>
                 </div>
                : <></>
                    :<>
                    <div className={`${classes.firstItem} ${classes.secondItem}`}>
                        <div className={classes.data}>
                            <b><FormattedMessage id={"harnesses.table_download_label"}/></b>
                        </div>
                        <div className={classes.data}>
                            <b><FormattedMessage id={"harnesses.table_delete_label"}/></b>
                        </div>
                    </div>
                </>
            }
        </div>
    );
}

export default HarnessesChooseTableItem;