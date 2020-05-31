import classes from "./CreateTaskPage.module.css"
import React from "react";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import FormControl from "@material-ui/core/FormControl";
import FormLabel from "@material-ui/core/FormLabel";
import RadioGroup from "@material-ui/core/RadioGroup";
import Radio from "@material-ui/core/Radio";
import SaveButton from "../../common/SaveButton/SaveButton";
import SuccessButton from "../../common/SuccessButton/SuccessButton";
import {withStyles} from "@material-ui/styles";
import {FormattedMessage} from "react-intl";
let CreateTaskPage = (props) => {
    const handleChangeWork = (event) => {
        props.setWorkType(event.target.value);
    };

    const handleChangeLoading = (event) => {
        props.setLoadingType(event.target.value);
    };

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
                                <input className={classes.input}/>
                            </label>
                        </div>

                        <div className={classes.input_wrapper}>
                            <label className={classes.label}>
                                <h3><FormattedMessage id={"tasks.create_new_task_harnesses_label"}/>:</h3>
                                <select className={classes.select}>

                                </select>
                            </label>
                        </div>

                        <div className={classes.input_wrapper}>
                            <label className={classes.label}>
                                <h3><FormattedMessage id={"tasks.create_new_task_komaxes_label"}/>:</h3>
                                <select className={classes.select}>

                                </select>
                            </label>
                        </div>

                        <div className={classes.input_wrapper}>
                            <label className={classes.label}>
                                <h3><FormattedMessage id={"tasks.create_new_task_kappas_label"}/>:</h3>
                                <select className={classes.select}>

                                </select>
                            </label>
                        </div>

                        <div className={classes.input_wrapper}>
                            <label className={classes.label}>
                                <h3><FormattedMessage id={"tasks.create_new_task_work_shift_label"}/>:</h3>
                                <input className={classes.input}/>
                            </label>
                        </div>
                    </div>
                    <div className={`${classes.column} ${classes.right}`}>
                        <div className={classes.options}>
                            {workType}
                            {loadingType}
                        </div>
                        <SuccessButton value={<FormattedMessage id={"tasks.create_new_task_continue_label"}/>} class={classes.addBtn}/>
                    </div>
                </div>
            </form>
            <form className={classes.form}>
                <FormattedMessage id={"tasks.create_new_task_fill_form_label"}/>
            </form>
        </div>
    )
}

export default CreateTaskPage;