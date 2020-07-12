import React from "react";
import classes from "./Infographics.module.css";
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import { easeQuadInOut } from 'd3-ease';
import AnimatedProgressProvider from "../AnimatedProgressProvider";


let Infographics = (props) => {
    const value1 = 70;
    const value2 = 40;
    const value3 = 35;
    let renderChart = (val) => {
        return (
            <AnimatedProgressProvider
              valueStart={0}
              valueEnd={val}
              duration={1.0}
              easingFunction={easeQuadInOut}
            >
                {(value) => {
                    const roundedValue = Math.round(value);
                    return (
                        <CircularProgressbar
                            value={roundedValue}
                            maxValue={100}
                            text={`До ${roundedValue}%`}
                            styles={buildStyles({
                                // Whether to use rounded or flat corners on the ends - can use 'butt' or 'round'
                                strokeLinecap: 'round',

                                // Text size
                                textSize: '16px',

                                // Colors
                                pathColor: `#d43a3a`,
                                textColor: '#d43a3a',
                                trailColor: 'gray',

                                pathTransition: 'none'
                          })}
                        />
                    )
                }}
            </AnimatedProgressProvider>
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