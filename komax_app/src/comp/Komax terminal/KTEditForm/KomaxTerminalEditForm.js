import classes from "./KomaxTerminalEditForm.module.css"
import React, {useState} from "react";
import FormControl from "@material-ui/core/FormControl";
import FormLabel from "@material-ui/core/FormLabel";
import RadioGroup from "@material-ui/core/RadioGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Radio from "@material-ui/core/Radio";
import {withStyles} from "@material-ui/styles";

let KomaxTerminalEditForm = (props) => {

    const handleChangeMaterial = (event) => {
        props.setMaterial(event.target.value);
    };

    const handleChangeTerminal = (event) => {
        props.setTerminal(event.target.value);
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

    let sealOptions = renderOptions(
        "Seal",
        props.materialValue,
        handleChangeMaterial,
        [
            {
                value : "False",
                label : "-"
            },
            {
                value : "True",
                label : "+"
            },
        ]
    );

    let terminalOptions = renderOptions(
        "Terminal",
        props.terminalAvaliable,
        handleChangeTerminal,
        [
            {
                value : "False",
                label : "-"
            },
            {
                value : "True",
                label : "+"
            },
        ]
    );

    return (
        <form className={classes.form}>
            <div className={classes.number}>
                <h2>{props.selected.terminal_number}</h2>
            </div>
            <div className={classes.options}>
                {sealOptions}
                {terminalOptions}
            </div>
            <button className={classes.saveBtn}>
                Сохранить
            </button>
        </form>
    );
}

export default KomaxTerminalEditForm;