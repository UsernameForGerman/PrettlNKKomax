import CreateTaskPage from "./CreateTaskPage";
import React, {useState} from "react";
import auth from "../../AuthHOC/authHOC";
import classes from "./CreateTaskPage.module.css"

let CreateTaskPageContainer = (props) => {
    let [workType, setWorkType] = useState("Parallel");
    let [loadingType, setLoadingType] = useState("New");
    return(
        <div className={classes.container}>
            <CreateTaskPage
                workType={workType}
                setWorkType={setWorkType}
                loadingType={loadingType}
                setLoadingType={setLoadingType}
            />
        </div>
    )
}

export default auth(CreateTaskPageContainer);