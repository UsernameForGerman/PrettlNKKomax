import classes from "./CreateTaskPage.module.css"
import React, {useState} from "react";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import FormControl from "@material-ui/core/FormControl";
import FormLabel from "@material-ui/core/FormLabel";
import RadioGroup from "@material-ui/core/RadioGroup";
import Radio from "@material-ui/core/Radio";
import SuccessButton from "../../common/SuccessButton/SuccessButton";
import {makeStyles, withStyles} from "@material-ui/styles";
import {FormattedMessage} from "react-intl";
import Select from "@material-ui/core/Select";
import Input from "@material-ui/core/Input";
import MenuItem from "@material-ui/core/MenuItem";
let CreateTaskPage = (props) => {

    let handleMultiSelect = (e, callback) => {
        callback(e.target.value);
    }

    let openNextForm = (e) => {
        e.preventDefault();
        props.setContinue(true);
        let data = {
            number : numberRef.current.value,
            work_shift : workShiftRef.current.value
        }
        props.sendDataFirst(data);
    }

    let collectData = (e) => {
        e.preventDefault();

        props.sendDataSecond({
            name : numberRef.current.value
        });
    }

    let renderedHarnesses = props.multiselectOptions.map(elem => {
        return(
            <label>
                {elem}
                <input placeholder={"Количество"} type={"number"} required onChange={(e) => {
                    props.addHarnessData(elem, e)
                }}/>
            </label>
        )
    })

    const handleChangeWork = (event) => {
        props.setWorkType(event.target.value);
    };

    const handleChangeLoading = (event) => {
        props.setLoadingType(event.target.value);
    };

    let numberRef = React.createRef();
    let workShiftRef = React.createRef();

    let checkValid = () => {
        let text = numberRef.current.value;
        props.check(text);
    }

    const CustomRadio = withStyles({
      root: {
        color: "gray",
        '&$checked': {
          color: "black",
        },
      },
      checked: {},
    })((props) => <Radio color="default" {...props} />);

    let renderOptions = (formName, value, onChange, options) => {
        let renderedOptions = options.map((option) => {
            return(
                <FormControlLabel value={option.value} control={<CustomRadio />} label={option.label} />
            );
        });
        return (
            <FormControl component="fieldset">
              <FormLabel component="legend">{formName}</FormLabel>
              <RadioGroup aria-label={formName} name={formName} value={value} onChange={onChange} row>
                  {renderedOptions}
              </RadioGroup>
            </FormControl>
        )
    }

    let workType = renderOptions(
        "Work type",
        props.workType,
        handleChangeWork,
        [
            {
                value : "Parallel",
                label : "Parallel"
            },
            {
                value : "Consistently",
                label : "Consistently"
            }
        ]
    );

    let loadingType = renderOptions(
        "Loading type",
        props.loadingType,
        handleChangeLoading,
        [
            {
                value : "New",
                label : "New"
            },
            {
                value : "Mix",
                label : "Mix"
            },
            {
                value : "Urgent",
                label : "Urgent"
            }
        ]
    );

    return(
        <div className={classes.formWrapper}>
            <form className={classes.form}>
                <div className={classes.heading}>
                    <h1><FormattedMessage id={"tasks.create_new_task_heading"}/></h1>
                </div>
                <div className={classes.row}>
                    <div className={classes.column}>
                        <div className={classes.input_wrapper}>
                            <label className={classes.label}>
                                <h3><FormattedMessage id={"tasks.create_new_task_job_name_label"}/>:</h3>
                                <input className={classes.input} required ref={numberRef} onChange={checkValid}/>
                            </label>
                        </div>

                        <div className={classes.input_wrapper}>
                            <label className={classes.label}>
                                <h3><FormattedMessage id={"tasks.create_new_task_harnesses_label"}/>:</h3>
                                <Select
                                  multiple
                                  classes={classes.select}
                                  value={props.multiselectOptions}
                                  onChange={(e) => {handleMultiSelect(e, props.setMultiselectOptions)}}
                                  input={<Input />}
                                >
                                  {props.harnesses_options.map((elem) => {
                                      return(
                                    <MenuItem key={elem} value={elem}>
                                        {elem}
                                    </MenuItem>
                                  )})}
                                </Select>
                            </label>
                        </div>

                        <div className={classes.input_wrapper}>
                            <label className={classes.label}>
                                <h3><FormattedMessage id={"tasks.create_new_task_komaxes_label"}/>:</h3>
                                <Select classes={classes.select}
                                  multiple
                                  value={props.komaxesOptions}
                                  onChange={(e) => {handleMultiSelect(e, props.setKomaxesOptions)}}
                                  input={<Input />}
                                >
                                  {props.komaxes_options.map((elem) => (
                                    <MenuItem key={elem} value={elem}>
                                      {elem}
                                    </MenuItem>
                                  ))}
                                </Select>
                            </label>
                        </div>

                        <div className={classes.input_wrapper}>
                            <label className={classes.label}>
                                <h3><FormattedMessage id={"tasks.create_new_task_kappas_label"}/>:</h3>
                                  <Select classes={classes.select}
                                      multiple
                                      value={props.kappasOptions}
                                      onChange={(e) => {handleMultiSelect(e, props.setKappasOptions)}}
                                      input={<Input />}
                                    >
                                      {props.kappas_options.map((elem) => (
                                        <MenuItem key={elem} value={elem}>
                                          {elem}
                                        </MenuItem>
                                      ))}
                                  </Select>
                            </label>
                        </div>

                        <div className={classes.input_wrapper}>
                            <label className={classes.label}>
                                <h3><FormattedMessage id={"tasks.create_new_task_work_shift_label"}/>:</h3>
                                <input className={classes.input} required type={"number"} ref={workShiftRef}/>
                            </label>
                        </div>
                    </div>
                    <div className={`${classes.column} ${classes.right}`}>
                        <div className={classes.options}>
                            {workType}
                            {loadingType}
                        </div>
                        <SuccessButton value={<FormattedMessage id={"tasks.create_new_task_continue_label"}/>} class={classes.addBtn} disable={!props.isValid} click={openNextForm}/>
                        <div className={classes.err}>
                            {props.errMsg}
                        </div>
                    </div>
                </div>
            </form>
            <form className={classes.form}>
                {!props.shouldContinue
                    ? <FormattedMessage id={"tasks.create_new_task_fill_form_label"}/>
                    : <form>
                        {renderedHarnesses}
                        <SuccessButton value={"Создать задание"} class={classes.addBtn} click={collectData} disable={!props.canSend}/>
                    </form>
                }
            </form>
        </div>
    )
}

export default CreateTaskPage;