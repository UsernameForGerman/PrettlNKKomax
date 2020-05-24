import classes from "./Header.module.css"
import React from "react";
import {NavLink} from "react-router-dom";
import logo from "../../assets/images/logo2.png"

let Header = (props) => {
    return(
        <>
            <div className={classes.Header}>
                <div className={classes.container}>
                    <div className={classes.tab}>
                        <NavLink to={"/"} className={classes.link} activeClassName={classes.activeLink}>
                            <button className={classes.button}>
                                Start
                            </button>
                        </NavLink>
                         <NavLink to={"/tasks"} className={classes.link} activeClassName={classes.activeLink}>
                            <button className={classes.button}>
                                Tasks
                            </button>
                        </NavLink>
                        <NavLink to={"/harnesses"} className={classes.link} activeClassName={classes.activeLink}>
                            <button className={classes.button}>
                                Harnesses
                            </button>
                        </NavLink>
                    </div>
                    <div className={classes.logoWrapper}>
                        <img src={logo} alt={"logo"} className={classes.logo}/>
                    </div>
                    <div className={classes.tab}>
                         <NavLink to={"/terminals"} className={classes.link} activeClassName={classes.activeLink}>
                            <button className={classes.button}>
                                Komax terminals
                            </button>
                        </NavLink>
                         <NavLink to={"/input"} className={classes.link} activeClassName={classes.activeLink}>
                            <button className={classes.button}>
                                Labor input
                            </button>
                        </NavLink>
                        <NavLink to={"/komaxes"} className={classes.link} activeClassName={classes.activeLink}>
                            <button className={classes.button}>
                                Komaxes
                            </button>
                        </NavLink>
                    </div>
                </div>
            </div>
            <div className={classes.spacing}/>
        </>
    )
}

export default Header;