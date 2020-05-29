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
import Preloader from "../Preloader/Preloader";
import harnessChartApi from "../../DAL/harness_chart/harness_chart_api";

let HarsessesContainer = (props) => {
    useEffect(() => {
        props.fetchList();
    }, props.list);

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
        "Harness number", "Провод", "Маркировка", "Номер", "Сечение", "Цвет", "Длина", "Армировка 1","Длина трубки 1", "Уплотнитель 1", "Частичное снятие 1", "Наконечник 1","Аппликатор 1", "Армировка 2","Длина трубки 2", "Уплотнитель 2", "Частичное снятие 2", "Наконечник 2","Аппликатор 2"
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

    let renderMap = () => {
        return(
            <>{props.isMapFetching
                ? <div className={classes.mapWrapper}><Preloader/></div>
                : selectedNumber.length > 0
                ? <div>
                    <h2>{"КРП " + selectedNumber}</h2>
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
                        Выберите жгут для просмотра его КРП
                    </h1>
                  </div>
              }
            </>
        );
    };

    return(
        <>{ props.isFetching
            ? <div className={classes.container_fluid}><Preloader/></div>
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

export default connect(mapStateToProps, mapDispatchToProps)(HarsessesContainer);
