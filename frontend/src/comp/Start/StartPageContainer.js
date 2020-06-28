import StartPage from "./StartPage";
import React from "react";
import auth from "../AuthHOC/authHOC";
import TaskItem from "../Tasks/TaskItem/TaskItem";
import ava from "../../assets/images/ava.png"

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
    ].map(elem => {
        return (
            <TaskItem {...elem}/>
        );
    })
    return(
        <StartPage {...user} tasks={items} role={"master"} ava={ava}/>
    )
}

export default auth(StartPageContainer);