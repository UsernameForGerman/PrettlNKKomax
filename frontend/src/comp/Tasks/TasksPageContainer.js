import React, {useEffect} from "react";
import TasksPage from "./TasksPage";
import auth from "../AuthHOC/authHOC";
import TaskItem from "./TaskItem/TaskItem";
import classes from "./TasksPage.module.css"
import {connect} from "react-redux";
import TasksSelector from "../../selectors/tasksSelector";
import {getTasksThunk} from "../../reducers/tasksReducer";
import FullScreenPreloader from "../common/Preloader/FullScreenPreloader";

let TasksPageContainer = (props) => {
    let user = {
        username : "master1"
    }
    useEffect(() => {
        props.fetchList();
    }, props.tasksList.length);

    let items = props.tasksList.map(elem => {
        return (
            <TaskItem {...elem}/>
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
                : <TasksPage rows={renderRows(items)} {...user}/>
            }
        </>
    )
}

let mapStateToProps = (state) => {
    return {
        isFetching : TasksSelector.getFetching(state),
        tasksList : TasksSelector.getList(state)
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        fetchList: () => {
            dispatch(getTasksThunk())
        }
    }
}

export default auth(connect(mapStateToProps, mapDispatchToProps)(TasksPageContainer));