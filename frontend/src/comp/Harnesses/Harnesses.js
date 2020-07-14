import classes from "./Harnesses.module.css"
import React from "react";
import HarnessesChooseTable from "./HarnessesTables/HarnessesChooseTable/HarnessesChooseTable";
import SuccessButton from "../common/SuccessButton/SuccessButton";
import {FormattedMessage} from "react-intl";
import BASE_URL from "../../DAL/getBaseUrl";
let Harnesses = (props) => {
    let send = (e) => {
        e.preventDefault();
        let req = new XMLHttpRequest();
        let data = new FormData(document.getElementById("form"));
        let token = window.localStorage.getItem('token');
        req.open('POST', BASE_URL + 'api/v1/harnesses/');
        req.setRequestHeader("Authorization", `Token ${token}`);
        req.send(data);
        req.onload = () => {
            props.fetch();
        }
    }

    let fileAttach = (e) => {
        alert("Файл " + e.target.files[0].name + " прикреплен");
    }
    return(
        <main className={classes.container}>
            <div className={classes.card}>
                <div className={classes.addHarness}>
                    <form className={classes.form} method={"post"} action={BASE_URL +"api/v1/harnesses/"} encType={"multipart/form-data"} id={"form"}>
                        <label>
                            <input type={"text"} name={"harness_number"} id={"harness_number"} placeholder={"Harness number"} className={classes.input} required/>
                        </label>
                        <input type={"file"} name={"harness_chart"} id={"harness_chart"} className={classes.file} required onChange={fileAttach}/>
                        <SuccessButton value={<FormattedMessage id={"add_button_text"}/>} click={send}/>
                    </form>
                </div>
                <HarnessesChooseTable role={props.role} items={props.harnesses}/>
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