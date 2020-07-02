import CreateTaskPage from "./CreateTaskPage";
import React, {useEffect, useRef, useState} from "react";
import auth from "../../AuthHOC/authHOC";
import classes from "./CreateTaskPage.module.css";
import {connect} from "react-redux";
import {getHarnessesListThunk} from "../../../reducers/harnessesReducer";
import {getListThunk} from "../../../reducers/komaxReducer";
import HarnessSelector from "../../../selectors/harnessSelector";
import KappaSelector from "../../../selectors/kappaSelector";
import KomaxSelector from "../../../selectors/komaxSelector";
import FullScreenPreloader from "../../common/Preloader/FullScreenPreloader";
import {getKappasThunk} from "../../../reducers/kappasReducer";
import TasksSelector from "../../../selectors/tasksSelector";
import {createTaskThunk, getTasksThunk, setErrorAC, setValidAC} from "../../../reducers/tasksReducer";
import {getSealsListThunk} from "../../../reducers/sealReducer";
import {getTerminalListThunk} from "../../../reducers/komaxTerminalReducer";

let CreateTaskPageContainer = (props) => {
    let [workType, setWorkType] = useState("parallel");
    let [loadingType, setLoadingType] = useState("new");
    let [multiselectOptions, setMultiselectOptions] = useState([]);
    let [shouldContinue, setContinue] = useState(false);
    let [harnessesData, setHarnessesData] = useState([]);
    let [komaxesOptions, setKomaxesOptions] = useState([]);
    let [kappasOptions, setKappasOptions] = useState([]);
    const mount = useRef(true);

    useEffect(() => {
        if (mount){
            props.fetchHarnesses();
            props.fetchKomaxes();
            props.fetchKappas();
            props.fetchKappas();
            props.fetchTasks();
        }
        return () => {
            mount.current = false;
        }
    },
        [
            props.harnesses.length
        ]);

    let harnesses_options = props.harnesses.map(elem => {
        return elem.harness_number;
    });

    let komaxes_options = props.komaxes.map(elem => {
        return elem.number;
    });

    let kappas_options = props.kappas.map(elem => {
        return elem.number;
    });

    let addHarnessData = (number, e) => {
        let data = harnessesData.filter(elem => elem[number]);
        let text = e.target.value;
        let arr = harnessesData.slice();
        if (data.length === 0){
            let obj = {};
            obj[number] = Number(text);
            arr.push(obj);
        } else {
            arr.map((elem) => {
                if (elem[number]) {
                    elem[number] = Number(text);
                }
            });
        }
        setHarnessesData(arr);
    }

    let check = (number) => {
        let numbers = props.tasks.map((elem) => {
            return elem.task_name;
        }).filter((elem) => elem === number);
        if (numbers.length > 0){
            props.setError("Такой номер уже есть");
            props.setValid(false);
        } else {
            props.setError("");
            props.setValid(true);
        }
    }

    let sendDataFirst = (data) => {
        debugger;
        let name = data.number;
        let shift = data.work_shift;
        let request = {
            'task_name' : name,
            'harnesses' : multiselectOptions,
            'komaxes' : komaxesOptions,
            'kappas' : kappasOptions,
            'shift' : shift,
            'type_of_allocation' : workType,
            'loading_type' : loadingType
        }

        props.send(request);
    }

    let sendDataSecond = (data) => {
        let d = {};
        harnessesData.forEach(harnessItem => {
            let key = Object.keys(harnessItem)[0];
            d[key] = harnessItem[key];
        })
        let request = {
            'harness_amount' : d,
            'task_name' : data.name
        }

        props.send(request);
    }

    let fetch = () => {
        props.fetchSeals();
        props.fetchTerminals();
    }

    return(
        <>
            <div className={classes.container}>
                    <CreateTaskPage
                        workType={workType}
                        setWorkType={setWorkType}
                        loadingType={loadingType}
                        setLoadingType={setLoadingType}
                        harnesses_options={harnesses_options}
                        komaxes_options={komaxes_options}
                        kappas_options={kappas_options}
                        isValid={props.isValid}
                        errMsg={props.errMsg}
                        check={check}
                        mount={mount}
                        multiselectOptions={multiselectOptions}
                        setMultiselectOptions={setMultiselectOptions}
                        shouldContinue={shouldContinue}
                        setContinue={setContinue}
                        addHarnessData={addHarnessData}
                        sendDataFirst={sendDataFirst}
                        sendDataSecond={sendDataSecond}
                        canSend={props.canSend}
                        fetch={fetch}
                        komaxesOptions={komaxesOptions}
                        setKomaxesOptions={setKomaxesOptions}
                        kappasOptions={kappasOptions}
                        setKappasOptions={setKappasOptions}
                    />
               </div>
        </>
    )
}

let mapStateToProps = (state) => {
    return{
        tasks : TasksSelector.getList(state),
        harnesses : HarnessSelector.getList(state),
        komaxes : KomaxSelector.getList(state),
        kappas : KappaSelector.getList(state),
        isFetching : HarnessSelector.getFetching(state) || KomaxSelector.getFetching(state) || KappaSelector.getFetching(state),
        errMsg : TasksSelector.getErrMsg(state),
        isValid : TasksSelector.getValid(state),
        canSend : TasksSelector.getCanSend(state)
    }
}

let mapDispatchToProps = (dispatch) => {
    return{
        fetchHarnesses : () => {
            dispatch(getHarnessesListThunk())
        },

        fetchKomaxes : () => {
            dispatch(getListThunk())
        },

        fetchKappas : () => {
            dispatch(getKappasThunk())
        },

        fetchTasks : () => {
            dispatch(getTasksThunk())
        },

        fetchSeals : () => {
            dispatch(getSealsListThunk());
        },

        fetchTerminals : () => {
            dispatch(getTerminalListThunk());
        },

        setError : (error) => {
            dispatch(setErrorAC(error))
        },

        setValid : (valid) => {
            dispatch(setValidAC(valid))
        },

        send : (task) => {
            dispatch(createTaskThunk(task))
        }
    }
}

export default auth(connect(mapStateToProps, mapDispatchToProps)(CreateTaskPageContainer));