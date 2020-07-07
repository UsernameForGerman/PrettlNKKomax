import classes from "./CreateTaskPage.module.css"
import React, {useState} from "react";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import FormControl from "@material-ui/core/FormControl";
import FormLabel from "@material-ui/core/FormLabel";
import RadioGroup from "@material-ui/core/RadioGroup";
import Radio from "@material-ui/core/Radio";
import SuccessButton from "../../common/SuccessButton/SuccessButton";
import {withStyles} from "@material-ui/styles";
import {FormattedMessage} from "react-intl";
import Select from "@material-ui/core/Select";
import Input from "@material-ui/core/Input";
import MenuItem from "@material-ui/core/MenuItem";
import IconButton from "../../common/IconButton/IconButton";
import Modal from "react-modal";
import TaskCreateModalFormContainer from "./Modal/TCPModalContainer,js";
import {Multiselect} from "multiselect-react-dropdown";
import '../../../index.css';
import {NavLink, Redirect} from "react-router-dom";
let CreateTaskPage = (props) => {
    const MenuProps = {
          PaperProps: {
            style: {
              width: 100,
              top: "100px !important"
            },
          },
        };
    const customStyles = {
      content : {
        top                   : '25%',
        left                  : '20%',
        transform             : 'translate(-10%, -20%)'
      }
    };

    let [isModalOpen, setIsOpen] = useState(false);
    let openModal = () => {
        setIsOpen(true);
    }

    let open = () => {
        openModal();
        props.fetch();
    }

    let closeModal = () => {
        setIsOpen(false)
    }

    let oldHandle = (e, callback) => {
        callback(e.target.value);
    }

    let handleMultiSelect = (e, callback) => {
        callback(e.map(elem => elem.name));
    }

    let openNextForm = (e) => {
        e.preventDefault();
        props.setContinue(true);
        let data = {
            number : numberRef.current.value,
            work_shift : workShiftRef.current.value,
        }
        props.sendDataFirst(data);
    }

    let collectData = (e) => {
        props.sendDataSecond({
            name : numberRef.current.value
        });
    }

    let renderedHarnesses = props.multiselectOptions.map(elem => {
        return(
            <label>
                {elem}
                <input placeholder={"Количество"} type={"number"} onChange={(e) => {
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
                value : "parallel",
                label : "Parallel"
            },
            {
                value : "consistently",
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
                value : "new",
                label : "New"
            },
            {
                value : "mix",
                label : "Mix"
            },
            {
                value : "urgent",
                label : "Urgent"
            }
        ]
    );

    let convertOptions = (src) => {
        return src.map(elem => {
            return {
                name: elem,
                id: elem
            }
        })
    }

    let harnesses_options = convertOptions(props.harnesses_options);

    return(
        <div className={classes.formWrapper}>
            <div className={classes.form}>
                <div className={classes.heading}>
                    <div className={classes.heading_text}><FormattedMessage id={"tasks.create_new_task_heading"}/></div>
                    <IconButton icon={["fas", 'cog']} class={classes.modalBtn} click={open}/>
                </div>
                <div className={classes.row}>
                    <div className={classes.column}>
                        <div className={classes.input_wrapper}>
                            <label className={classes.label}>
                                <h3><FormattedMessage id={"tasks.create_new_task_job_name_label"}/>:</h3>
                                <input className={classes.input} ref={numberRef} onChange={checkValid}/>
                            </label>
                        </div>

                        <div className={classes.input_wrapper}>
                            <label className={classes.label}>
                                <div><FormattedMessage id={"tasks.create_new_task_harnesses_label"}/>:</div>
                                <div className={classes.multiselect_wrapper}>
                                    <Multiselect
                                        options={harnesses_options}
                                        onSelect={(e) => {handleMultiSelect(e, props.setMultiselectOptions)}}
                                        onRemove={(e) => {handleMultiSelect(e, props.setMultiselectOptions)}}
                                        selectedValues={props.multiselectOptions.map(elem => {return {name : elem, id : elem}})}
                                        displayValue="name"
                                        style={{
                                              multiselectContainer: { // To change css for multiselect (Width,height,etc..)
                                                width : "200px"
                                              }
                                        }}
                                        id={"harnesses_select"}
                                    />
                                </div>
                            </label>
                        </div>

                        <div className={classes.input_wrapper}>
                            <label className={classes.label}>
                                <h3><FormattedMessage id={"tasks.create_new_task_komaxes_label"}/>:</h3>
                                <Select classes={classes.select}
                                  multiple
                                  value={props.komaxesOptions}
                                  onChange={(e) => {oldHandle(e, props.setKomaxesOptions)}}
                                  input={<Input />}
                                    MenuProps={MenuProps}
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
                                      onChange={(e) => {oldHandle(e, props.setKappasOptions)}}
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
                                <input className={classes.input} type={"number"} ref={workShiftRef}/>
                            </label>
                        </div>
                    </div>
                    <div className={`${classes.column} ${classes.right}`}>
                        <div className={classes.options}>
                            {workType}
                            {loadingType}
                        </div>
                        <SuccessButton value={<FormattedMessage id={"tasks.create_new_task_continue_label"}/>} class={classes.addBtn} disable={!props.isValid || props.shouldContinue} click={openNextForm}/>
                        <div className={classes.err}>
                            {props.errMsg}
                        </div>
                    </div>
                </div>
            </div>
            <form className={classes.form}>
                {!props.shouldContinue
                    ? <button disabled className={classes.fill}>
                            <FormattedMessage id={"tasks.create_new_task_fill_form_label"}/>
                      </button>
                    : <form className={classes.right_form}>
                        <div className={classes.list}>
                            {renderedHarnesses}
                        </div>
                        <NavLink to={"/tasks"} onClick={collectData}>
                            <SuccessButton value={"Создать задание"} class={classes.addBtn} disable={!props.canSend}/>
                        </NavLink>
                    </form>
                }
            </form>
            <Modal
              isOpen={isModalOpen}
              onRequestClose={closeModal}
              style={customStyles}
              contentLabel="Example Modal"
            >
                <TaskCreateModalFormContainer close={closeModal}/>
            </Modal>
        </div>
    )
}

export default CreateTaskPage;