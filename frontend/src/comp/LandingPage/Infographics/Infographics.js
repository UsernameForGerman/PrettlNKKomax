import React from "react";
import classes from "./Infographics.module.css";
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

let Infographics = (props) => {
    const value1 = 0.7;
    const value2 = 0.4;
    const value3 = 0.35;
    let renderChart = (val) => {
        return (
            <CircularProgressbar
                value={val}
                maxValue={1}
                text={`До ${val * 100}%`}
                styles={buildStyles({
                    // Whether to use rounded or flat corners on the ends - can use 'butt' or 'round'
                    strokeLinecap: 'round',

                    // Text size
                    textSize: '16px',

                    // Colors
                    pathColor: `#d43a3a`,
                    textColor: '#d43a3a',
                    trailColor: 'gray'
              })}
            />
        )
    }
    return (
        <section className={classes.infographics}>
            <div className={classes.info}>
                <div className={classes.graph}>
                    {renderChart(value1)}
                </div>
                <div className={classes.desc}>
                    Рост произв-ти единицы пр-ва
                </div>
            </div>
            <div className={classes.info}>
                <div className={classes.graph}>
                    {renderChart(value2)}
                </div>
                <div className={classes.desc}>
                    Cнижение стоимости поставки
                </div>
            </div>
            <div className={classes.info}>
                <div className={classes.graph}>
                    {renderChart(value3)}
                </div>
                <div className={classes.desc}>
                    Рост возвращаемости клиента
                </div>
            </div>
        </section>
    )
}

export default Infographics;