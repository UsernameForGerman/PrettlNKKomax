import React from "react";
import TasksPage from "./TasksPage";
import auth from "../AuthHOC/authHOC";
import TaskItem from "./TaskItem/TaskItem";
import classes from "./TasksPage.module.css"
import task_api from "../../DAL/task/task_api";

let TasksPageContainer = (props) => {
    let user = {
        username : "master1"
    }
    let items = [
        {
            number : "11000-132",
            status : 1,
            link : "/"
        },
        {
            number : "13241-1387",
            status : 2,
            link : "/"
        },
        {
            number : "768-01342",
            status : 3,
            link : "/"
        },
        {
            number : "1423-132",
            status : 2,
            link : "/"
        },
        {
            number : "13241-1387",
            status : 3,
            link : "/"
        },
        {
            number : "73213-13",
            status : 1,
            link : "/"
        },
        {
            number : "13241-1387",
            status : 3,
            link : "/"
        },
        {
            number : "73213-13",
            status : 1,
            link : "/"
        }
    ].map(elem => {
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

    task_api.getKomaxTasks().then(console.log);

    return(
        <TasksPage rows={renderRows(items)} {...user}/>
    )
}

export default auth(TasksPageContainer);