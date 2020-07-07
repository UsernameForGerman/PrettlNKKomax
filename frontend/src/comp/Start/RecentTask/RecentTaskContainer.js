import RecentTask from "./RecentTask";
import React, {useEffect} from "react";
import classes from "./RecentTask.module.css"
import {connect} from "react-redux";
import {getStatusThunk} from "../../../reducers/tasksReducer";
import TasksSelector from "../../../selectors/tasksSelector";
import LinearProgress from "@material-ui/core/LinearProgress";
import BASE_URL from "../../../DAL/getBaseUrl";
import LoginSelector from "../../../selectors/loginSelector";
let RecentTaskContainer = (props) => {
    useEffect(() => {
        props.getStatus();
    }, [props.status.harnesses.length]);

    let komaxes = props.status.komax_task !== undefined ? props.status.komax_task.komaxes : [];

    let harnesses =  props.status.harnesses ? props.status.harnesses : [];

    let name = props.status.komax_task !== undefined ? props.status.komax_task.task_name : -1;

    let ticket_komax = komaxes.map(elem => {
        return(
            <a href={BASE_URL + "tasks/" + name +"/get_ticket_komax/" + elem.komax +"/"} target={"blank"}>
                <button className={classes.greenBtn}>
                    Ticket {elem.komax}
                </button>
            </a>
        )
    });

    let harnesses_btns = harnesses.map(elem => {
        let percent = isNaN(elem.left_time_secs / elem.sum_time_secs) ? 0 : (elem.left_time_secs / elem.sum_time_secs) * 100;
        return(
            <div className={classes.harness}>
                <div className={classes.harness_heading}>
                    {elem.harness_number}
                </div>
                <div className={classes.status}>
                    {percent} % completed
                    <LinearProgress variant="determinate" value={percent} />
                </div>
                <a href={BASE_URL + "harnesses/" + elem.harness_number +"/download/"} target={"blank"}>
                    <button className={classes.greenBtn}>
                        Download
                    </button>
                </a>
            </div>
        )
    });

    return (
        <>
            {name + "" === "-1" || props.role.toString().toLowerCase() !== ("master" || "operator")
                ? <></>
                : <RecentTask {...props} tickets={ticket_komax} harnesses={harnesses_btns} number={name}/>
            }
        </>
    )
}

let mapStateToProps = (state) => {
    return {
        status : TasksSelector.getStatus(state),
        role : LoginSelector.getRole(state)
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        getStatus : () => {
            dispatch(getStatusThunk())
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(RecentTaskContainer);