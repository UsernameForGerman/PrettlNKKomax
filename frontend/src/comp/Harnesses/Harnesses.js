import classes from "./Harnesses.module.css"
import React from "react";
import HarnessesChooseTable from "./HarnessesTables/HarnessesChooseTable/HarnessesChooseTable";
import SuccessButton from "../common/SuccessButton/SuccessButton";
import {FormattedMessage} from "react-intl";
import file from "../../assets/docs/6282-2124813-12.xlsx"
let Harnesses = (props) => {
    let send = (e) => {
        let body = 'harness_number=' + encodeURIComponent("44-11-2") +
                    '&harness_chart=' + encodeURIComponent(document.getElementById('harness_chart').value);
        e.preventDefault();
        let req = new XMLHttpRequest();
        req.open('POST', 'http://localhost:8000/api/v2/harnesses/');
        req.setRequestHeader('Authorization', 'Token ' + window.localStorage.getItem('token'));
        req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        req.send(body);

        req.onload(() => {
            debugger;
            console.log("Loaded");
        })
    }
    return(
        <main className={classes.container}>
            <div className={classes.card}>
                <div className={classes.addHarness}>
                    <form className={classes.form} method={"post"} action={"http://localhost:8000/api/v2/harnesses/"} enctype="multipart/form-data">
                        <label>
                            <FormattedMessage id={"harnesses.add_harness_number_placeholder"}/>
                            <input type={"text"} name={"harness_number"} id={"harness_number"} value={"6282-2124813-12"} className={classes.input}/>
                        </label>
                        <input type={"file"} name={"harness_chart"} id={"harness_chart"} className={classes.file}/>
                        <div className={classes.response}>
                            <strong>OK</strong>
                        </div>
                        <SuccessButton value={<FormattedMessage id={"add_button_text"}/>}/>
                        <button onClick={send}>Добавить</button>
                    </form>
                </div>
                <HarnessesChooseTable items={props.harnesses}/>
            </div>
            <div className={`${classes.card} ${classes.tableWrapper}`}>
                {props.selectedTable
                    ? <>{props.selectedTable}</>
                    : <>
                        <FormattedMessage id={"harnesses.choose_terminal"}/>
                      </>
                }
            </div>
        </main>
    );
}

export default Harnesses;