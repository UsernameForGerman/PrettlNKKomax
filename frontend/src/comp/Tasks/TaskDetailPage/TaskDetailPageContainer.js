import TaskDetailPage from "./TaskDetailPage";
import React, {useEffect} from "react";
import {withRouter} from "react-router-dom";
import auth from "../../AuthHOC/authHOC";
import {connect} from "react-redux"
import classes from "./TaskDetailPage.module.css"
import TasksSelector from "../../../selectors/tasksSelector";
import {getTasksThunk} from "../../../reducers/tasksReducer";

let TaskDetailPageContainer = (props) => {
    let name = props.match.params.id;

    useEffect(() => {
        props.fetchList();
    }, props.taskList.length);

    /*
    let task = props.taskList.filter(elem => elem.task_name === name)[0];
    let komaxes = task.komaxes;
    let harnesses = task.harnesses;
    debugger;

     */

    let harnesses = [{
        harness : "14",
        amount : 2
    }]
    let komaxes = [{
        komax : "15",
        time : 2
    }]
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
            <button className={classes.greenBtn}>
                Task {elem.komax}
            </button>
        )
    });

    let ticket_komax = komaxes.map(elem => {
        return(
            <button className={classes.greenBtn}>
                Ticket {elem.komax}
            </button>
        )
    });

    return(
        <TaskDetailPage
        task_komax={task_komax}
        ticket_komax={ticket_komax}
        harnesses={taskHarnesses}
        komaxes={taskKomaxes}
        />
    )
}

let mapStateToProps = (state) => {
    return{
        taskList : TasksSelector.getList(state)
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