import React from "react";
import classes from "./RemoveBtn.module.css";
import BASE_URL from "../../../../DAL/getBaseUrl";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
let RemoveBtn = (props) => {
    let stopTask = () => {
        let path = BASE_URL + "api/v1/" + props.task_name + "/stop/";
        let token = window.localStorage.getItem('token');
        let req = new XMLHttpRequest();
        req.open('POST', path);
        req.setRequestHeader("Authorization", `Token ${token}`);
        req.send();
    }

    let deleteTask = () => {

    }

    let isMaster = props.role.toString().toLowerCase() === "master";

    let delBtn = (<button className={classes.btn} onClick={deleteTask}>
                        <FontAwesomeIcon icon={['fas', 'trash-alt']}/>
                    </button>);
    let stopBtn = (<button className={classes.btn} onClick={stopTask}>
                        <FontAwesomeIcon icon={['fas', 'stop']}/>
                    </button>);
    return (
        <>
            {isMaster
                ?   props.status === 3
                        ? stopBtn
                        : delBtn
                :   delBtn
            }
        </>
    )
}

export default RemoveBtn;