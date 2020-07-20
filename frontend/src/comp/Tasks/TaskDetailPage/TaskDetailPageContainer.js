import TaskDetailPage from "./TaskDetailPage";
import React, {useEffect} from "react";
import {withRouter} from "react-router-dom";
import auth from "../../AuthHOC/authHOC";
import {connect} from "react-redux"
import classes from "./TaskDetailPage.module.css"
import TasksSelector from "../../../selectors/tasksSelector";
import {getTasksThunk} from "../../../reducers/tasksReducer";
import LoginSelector from "../../../selectors/loginSelector";
import BASE_URL from "../../../DAL/getBaseUrl";
import formatTime from "./formatTime";
import {FormattedMessage} from "react-intl";

let TaskDetailPageContainer = (props) => {
    let name = props.match.params.id;

    useEffect(() => {
        props.fetchList();
    }, props.taskList.length);

    let task = props.taskList.filter(elem => elem.task_name === name)[0];
    let komaxes = task ? task.komaxes: []
    let harnesses = task ? task.harnesses : [];

    let taskHarnesses = harnesses.map((elem, index) => {
        return(
            <h3 className={classes.harness}>
                {elem.harness} : {elem.amount}
            </h3>
        )
    });

    let taskKomaxes = komaxes.map(elem => {
        return(
            <h3 className={classes.komax}>
                <div style={{
                    minWidth : "50px",
                    textAlign : "right"
                }}>{elem.komax} - </div>
                <div style={{
                    minWidth : "150px",
                    textAlign : "left"
                }}>{formatTime(elem.time, props.locale)}</div>
            </h3>
        )
    });

    let row = [];
    let task_komax = komaxes.map((elem, index) => {
        row.push(
            <a href={BASE_URL + "api/v1/" + name +"/get_task_komax/" + elem.komax +"/"} target={"blank"}>
                <button className={classes.greenBtn}>
                    <FormattedMessage id={"task_label"}/> {elem.komax}
                </button>
            </a>
        )

        if ((index + 1) % 3 === 0){
            let result =
             (
                <div className={classes.row}>
                    {[...row]}
                </div>
            )
            row = [];
            return result;
        } else {
            return (<></>)
        }
    });
    if (row.length > 0){
        task_komax.push(
                <div className={classes.row}>
                    {[...row]}
                </div>)
            row = [];
    }
    row = [];

    let ticket_komax = komaxes.map((elem, index) => {
        row.push(
            <a href={BASE_URL + "api/v1/" + name +"/get_ticket_komax/" + elem.komax +"/"} target={"blank"}>
                <button className={classes.greenBtn}>
                    <FormattedMessage id={"ticket_label"}/> {elem.komax}
                </button>
            </a>
        )
        if ((index + 1) % 3 === 0){
            let result =
             (
                <div className={classes.row}>
                    {[...row]}
                </div>
            )
            row = [];
            return result;
        } else {
            return (<></>)
        }
    });
    if (row.length > 0){
        task_komax.push(
                <div className={classes.row}>
                    {[...row]}
                </div>)
            row = [];
    }

    return(
        <TaskDetailPage
            role={props.role}
        task_komax={task_komax}
        ticket_komax={ticket_komax}
        harnesses={taskHarnesses}
        komaxes={taskKomaxes}
        name={name}
        />
    )
}

let mapStateToProps = (state) => {
    return{
        taskList : TasksSelector.getList(state),
        role : LoginSelector.getRole(state)
    }
}

let mapDispatchToProps = (dispatch) => {
    return{
        fetchList : () => {
            dispatch(getTasksThunk())
        }
    }
}

export default auth(withRouter(connect(mapStateToProps, mapDispatchToProps)(TaskDetailPageContainer)));