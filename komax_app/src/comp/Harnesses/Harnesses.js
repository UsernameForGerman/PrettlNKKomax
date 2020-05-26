import classes from "./Harnesses.module.css"
import React from "react";
import HarnessesChooseTable from "./HarnessesTables/HarnessesChooseTable/HarnessesChooseTable";
let Harnesses = (props) => {
    return(
        <main className={classes.container}>
            <div className={classes.card}>
                <div className={classes.addHarness}>
                    <form className={classes.form}>
                        <input type={"text"} className={classes.input} placeholder={"Harnesses number"}/>
                        <input type={"file"} className={classes.file}/>
                        <div className={classes.response}>
                            <strong>OK</strong>
                        </div>
                        <button className={classes.succBtn}>
                            Добавить
                        </button>
                    </form>
                </div>
                <HarnessesChooseTable items={props.harnesses}/>
            </div>
            <div className={`${classes.card} ${classes.tableWrapper}`}>
                {props.selectedTable
                    ? <>{props.selectedTable}</>
                    : <>
                        Выберите жгут из таблицы и здесь появится карта резки
                      </>
                }
            </div>
        </main>
    );
}

export default Harnesses;