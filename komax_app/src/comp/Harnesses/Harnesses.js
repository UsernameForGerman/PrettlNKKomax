import classes from "./Harnesses.module.css"
import React from "react";
import HarnessesChooseTable from "./HarnessesTables/HarnessesChooseTable/HarnessesChooseTable";
import SuccessButton from "../common/SuccessButton/SuccessButton";
import {FormattedMessage} from "react-intl";
let Harnesses = (props) => {
    return(
        <main className={classes.container}>
            <div className={classes.card}>
                <div className={classes.addHarness}>
                    <form className={classes.form}>
                        <label>
                            <FormattedMessage id={"harnesses.add_harness_number_placeholder"}/>
                            <input type={"text"} className={classes.input}/>
                        </label>
                        <input type={"file"} className={classes.file}/>
                        <div className={classes.response}>
                            <strong>OK</strong>
                        </div>
                        <SuccessButton value={<FormattedMessage id={"komax.add_button_text"}/>}/>
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