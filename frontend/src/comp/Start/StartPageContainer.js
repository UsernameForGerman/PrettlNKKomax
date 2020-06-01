import StartPage from "./StartPage";
import React from "react";
import auth from "../AuthHOC/authHOC";
import TaskItem from "../Tasks/TaskItem/TaskItem";

let StartPageContainer = (props) => {
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
        }
    ].map(elem => {
        return (
            <TaskItem {...elem}/>
        );
    })
    return(
        <StartPage {...user} tasks={items}/>
    )
}

export default auth(StartPageContainer);