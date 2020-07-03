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

let TaskDetailPageContainer = (props) => {
    debugger;
    let name = props.match.params.id;

    useEffect(() => {
        props.fetchList();
    }, props.taskList.length);

    let task = props.taskList.filter(elem => elem.task_name === name)[0];
    let komaxes = task ? task.komaxes: []
    let harnesses = task ? task.harnesses : [];

    let taskHarnesses = harnesses.map(elem => {
        return(
            <h3 className={classes.harness}>
                {elem.harness} : {elem.amount}
            </h3>
        )
    });

    let taskKomaxes = komaxes.map(elem => {
        return(
            <h3 className={classes.komax}>
                {elem.komax} - {elem.time}
            </h3>
        )
    });

    let task_komax = komaxes.map(elem => {
        return(
            <a href={BASE_URL + "tasks/" + name +"/get_task_komax/" + elem.komax +"/"} target={"blank"}>
                <button className={classes.greenBtn}>
                    Task {elem.komax}
                </button>
            </a>
        )
    });

    let ticket_komax = komaxes.map(elem => {
        return(
            <a href={BASE_URL + "tasks/" + name +"/get_ticket_komax/" + elem.komax +"/"} target={"blank"}>
                <button className={classes.greenBtn}>
                    Ticket {elem.komax}
                </button>
            </a>
        )
    });

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
        role : LoginSelector.getLogin(state)
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