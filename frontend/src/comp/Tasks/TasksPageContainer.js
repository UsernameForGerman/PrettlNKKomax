import React, {useEffect} from "react";
import TasksPage from "./TasksPage";
import auth from "../AuthHOC/authHOC";
import TaskItem from "./TaskItem/TaskItem";
import classes from "./TasksPage.module.css"
import {connect} from "react-redux";
import TasksSelector from "../../selectors/tasksSelector";
import {deleteTaskThunk, getTasksThunk} from "../../reducers/tasksReducer";
import FullScreenPreloader from "../common/Preloader/FullScreenPreloader";
import LoginSelector from "../../selectors/loginSelector";

let TasksPageContainer = (props) => {
    let user = {
        username : props.login
    }
    useEffect(() => {
        props.fetchList();
    }, props.tasksList.length);

    let items = props.tasksList.sort((a,b) => {
        return Number(b.task_name) - Number(a.task_name);
    }).map(elem => {
        return (
            <TaskItem {...elem} role={props.role} komax={props.komax} delete={props.deleteTask}/>
        );
    });

    let renderRows = (items) => {
        let rows = [];
        let row = [];
        for (let i = 0; i < items.length; i++){
            row.push(items[i]);
            if (i % 3 === 2){
                rows.push(
                    (
                        <div className={classes.recentTasks}>
                            {row}
                        </div>
                    )
                );
                row = [];
            }
        }
        if (row.length > 0){
            rows.push(
                (
                    <div className={classes.recentTasks}>
                        {row}
                    </div>
                )
            );
        }

        return rows;
    }

    return(
        <>
            {props.isFetching
                ? <FullScreenPreloader/>
                : <TasksPage rows={renderRows(items)} {...user} role={props.role}/>
            }
        </>
    )
}

let mapStateToProps = (state) => {
    return {
        isFetching : TasksSelector.getFetching(state),
        tasksList : TasksSelector.getList(state),
        login : LoginSelector.getLogin(state),
        role : LoginSelector.getRole(state),
        komax : LoginSelector.getKomax(state)
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        fetchList: () => {
            dispatch(getTasksThunk())
        },

        deleteTask: (task) => {
            dispatch(deleteTaskThunk(task))
        }
    }
}

export default auth(connect(mapStateToProps, mapDispatchToProps)(TasksPageContainer));