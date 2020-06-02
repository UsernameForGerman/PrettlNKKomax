import Harnesses from "./Harnesses";
import React, {useEffect, useState} from "react";
import HarnessesChooseTableItem from "./HarnessesTables/HarnessesChooseTable/Item/HCTItem";
import TableContainer from "@material-ui/core/TableContainer";
import Table from "@material-ui/core/Table";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import TableBody from "@material-ui/core/TableBody";
import Paper from "@material-ui/core/Paper";
import classes from "./Harnesses.module.css"
import HarnessSelector from "../../selectors/harnessSelector";
import {deleteHarnessByNumberThunk, getChartByNumberThunk, getHarnessesListThunk} from "../../reducers/harnessesReducer";
import {connect} from "react-redux";
import Preloader from "../common/Preloader/Preloader";
import harnessApi from "../../DAL/harness/harnessApi";
import {FormattedMessage} from "react-intl";
import auth from "../AuthHOC/authHOC";
import FullScreenPreloader from "../common/Preloader/FullScreenPreloader";
import file from "../../assets/docs/6282-2124813-12.xlsx";

let HarsessesContainer = (props) => {
    useEffect(() => {
        props.fetchList();
    }, props.list.length);

    let [selectedNumber, setSelectedNumber] = useState("");

    let items = props.list;

    items = items.map((elem) => {
        let deleteHarness = () => {
            props.deleteHarness(elem.harness_number);
        }

        let select = () => {
            setSelectedNumber(elem.harness_number);
            props.fetchMap(elem.harness_number)
        }

        return(
          <HarnessesChooseTableItem {...elem} select={select} delete={deleteHarness}/>
        );
    });

    let headings = [
        <FormattedMessage id={"harnesses.map_harnesses_number"}/>, <FormattedMessage id={"harnesses.map_harness"}/>, <FormattedMessage id={"harnesses.map_marking"}/>, <FormattedMessage id={"harnesses.map_wire_number"}/>, <FormattedMessage id={"harnesses.map_wire_square"}/>, <FormattedMessage id={"harnesses.map_wire_color"}/>, <FormattedMessage id={"harnesses.map_wire_length"}/>, <FormattedMessage id={"harnesses.map_armirovka"}/>, <FormattedMessage id={"harnesses.map_tube_len"}/>, <FormattedMessage id={"harnesses.map_wire_seal"}/>, <FormattedMessage id={"harnesses.map_wire_cut_length"}/>, <FormattedMessage id={"harnesses.map_wire_terminal"}/>, <FormattedMessage id={"harnesses.map_aplicator"}/>, <FormattedMessage id={"harnesses.map_armirovka_2"}/>, <FormattedMessage id={"harnesses.map_tube_len_2"}/>, <FormattedMessage id={"harnesses.map_wire_seal_2"}/>, <FormattedMessage id={"harnesses.map_wire_cut_length_2"}/>, <FormattedMessage id={"harnesses.map_wire_terminal_2"}/>, <FormattedMessage id={"harnesses.map_aplicator_2"}/>
    ].map((heading) => {
        return(<TableCell align="right"><b>{heading}</b></TableCell>)
    });

    let renderRows = (list) => {
        let order = ['id', 'harness', 'wire_type', 'marking', 'wire_number', 'wire_square', 'wire_color', 'wire_length', 'armirovka_1', 'tube_len_1', 'wire_seal_1', 'wire_cut_length_1', 'wire_terminal_1', 'aplicator_1', 'armirovka_2', 'tube_len_2', 'wire_seal_2', 'wire_cut_length_2', 'wire_terminal_2', 'aplicator_2'];

        list = list.map((row) => {
            row = Object.keys(row).map((elem, index) => {
                let key = order[index];
                let value = row[key];
                return(
                    <TableCell align="right">{value}</TableCell>
                )
            });

            return(
                <TableRow>
                    {row}
                </TableRow>
            );
        });

        return list;
    }

    let rows = renderRows(props.selectedMap);

    harnessApi.createHarness("6282-2124813-15", file).then(console.log);

    let renderMap = () => {
        return(
            <>{props.isMapFetching
                ? <div className={classes.mapWrapper}><Preloader/></div>
                : selectedNumber.length > 0
                ? <div>
                    <h2><FormattedMessage id={"harnesses.map_name"}/>{" " + selectedNumber}</h2>
                      <TableContainer component={Paper} className={classes.table}>
                      <Table aria-label="simple table">
                        <TableHead>
                          <TableRow>
                            <TableCell><b>#</b></TableCell>
                              {headings}
                          </TableRow>
                        </TableHead>
                        <TableBody>
                            {rows}
                        </TableBody>
                      </Table>
                    </TableContainer>
                  </div>
                : <div className={classes.mapWrapper}>
                    <h1>
                        <FormattedMessage id={"harnesses.choose_terminal"}/>
                    </h1>
                  </div>
              }
            </>
        );
    };

    harnessApi.createHarness("4444-232", file).then(console.log);

    return(
        <>{ props.isFetching
            ? <FullScreenPreloader/>
            : <Harnesses harnesses={items} selectedTable={renderMap()}/>
          }
        </>
    )
}

let mapStateToProps = (state) => {
    return {
        list : HarnessSelector.getList(state),
        isFetching : HarnessSelector.getFetching(state),
        isMapFetching : HarnessSelector.getMapFetching(state),
        selectedMap : HarnessSelector.getMap(state)
    }
}

let mapDispatchToProps = (dispatch) => {
    return {
        fetchList : () => {
            dispatch(getHarnessesListThunk());
        },

        deleteHarness : (number) => {
            dispatch(deleteHarnessByNumberThunk(number));
        },

        fetchMap : (number) => {
            dispatch(getChartByNumberThunk(number))
        }
    }
}

export default auth(connect(mapStateToProps, mapDispatchToProps)(HarsessesContainer));
