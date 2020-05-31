import classes from "./AddForm.module.css"
import React from "react";
import {FormattedMessage} from "react-intl";
import {withStyles} from "@material-ui/styles";
import Radio from "@material-ui/core/Radio";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import FormControl from "@material-ui/core/FormControl";
import FormLabel from "@material-ui/core/FormLabel";
import RadioGroup from "@material-ui/core/RadioGroup";
import SuccessButton from "../../common/SuccessButton/SuccessButton";
let AddForm = (props) => {
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
        <FormattedMessage id={"terminal.material_avaliable_label"}/>,
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
        <FormattedMessage id={"terminal.terminal_avaliable_label"}/>,
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
    return(
        <form className={classes.form}>
            <label>
                <FormattedMessage id={"terminal.terminal_number_label"}/>
                <input className={classes.input} type={"text"}/>
            </label>
            {sealOptions}
            {terminalOptions}
            <SuccessButton class={classes.btn} value={<FormattedMessage id={"add_button_text"}/>}/>
        </form>
    )
}

export default AddForm;