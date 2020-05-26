import Harnesses from "./Harnesses";
import React from "react";
import HarnessesChooseTableItem from "./HarnessesTables/HarnessesChooseTable/Item/HCTItem";
import TableContainer from "@material-ui/core/TableContainer";
import Table from "@material-ui/core/Table";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import TableBody from "@material-ui/core/TableBody";
import Paper from "@material-ui/core/Paper";
import classes from "./Harnesses.module.css"

let HarsessesContainer = (props) => {
        let items = [
        {
            number : "441-4532-23",
            date : "03.03.2002"
        },
        {
            number : "4231-452-28",
            date : "12.04.2012"
        },
        {
            number : "632-2453-10",
            date : "04.07.2020"
        },
        {
            number : "818-4532-48",
            date : "10.01.2010"
        },
    ];

    items = items.map((elem) => {
        return(
          <HarnessesChooseTableItem {...elem}/>
        );
    });

    let generateData = (length) => {
        let array = [];
        for (let i = 0; i < length; i++){
            let number = Math.floor(Math.random() * 1000);
            array.push(number);
        }

        return array;
    }

    let headings = [
        "Harness number", "Harness number", "Harness number", "Harness number", "Harness number", "Harness number", "Harness number", "Harness number","Harness number", "Harness number", "Harness number", "Harness number","Harness number", "Harness number", "Harness number", "Harness number","Harness number", "Harness number", "Harness number", "Harness number"
    ].map((heading) => {
        return(<TableCell align="right"><b>{heading}</b></TableCell>)
    });

    let itemsCount = 10;
    let renderRows = (length) => {
        let array = [];
        for (let i = 0; i < length; i++){
            array.push(Object.values({...generateData(headings.length + 1)}));
        }

        array = array.map((row) => {
            row = row.map((elem) => {
                return(
                    <TableCell align="right">{elem}</TableCell>
                )
            });

            return(
                <TableRow>
                    {row}
                </TableRow>
            );
        });

        return array;
    }
    let rows = renderRows(itemsCount);

    let renderMap = () => {
        return(
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
        );
    };

    return(
        <Harnesses harnesses={items} selectedTable={renderMap()}/>
    )
}

export default HarsessesContainer;
