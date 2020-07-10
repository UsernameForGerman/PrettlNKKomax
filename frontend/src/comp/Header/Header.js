import classes from "./Header.module.css"
import React, {useState} from "react";
import {NavLink, Redirect} from "react-router-dom";
import logo from "../../assets/images/logo2.png"
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";

import MenuIcon from '@material-ui/icons/Menu';

import Drawer from "@material-ui/core/Drawer";
import List from "@material-ui/core/List";
import IconButton from "@material-ui/core/IconButton";
import ListItemIcon from "@material-ui/core/ListItemIcon";

import {Briefcase, Clock, Folder, GitCommit, Home, Settings} from "react-feather";
import {FormattedMessage} from "react-intl";
import get_pages from "../AuthHOC/get_pages";

let Header = (props) => {
    let availablePages = get_pages(props.role);
    let buttonsState = [
        {
          desc : <FormattedMessage id={"header.start_link"}/>,
          link : "/"
        },
        {
          desc : <FormattedMessage id={"header.tasks_link"}/>,
          link : "/tasks"
        },
        {
          desc : <FormattedMessage id={"header.harnesses_link"}/>,
          link : "/harnesses"
        },
        {
          desc : <FormattedMessage id={"header.komax_teminals_link"}/>,
          link : "/terminals"
        },
        {
          desc : <FormattedMessage id={"header.labour_inputs_link"}/>,
          link : "/labour"
        },
        {
          desc : <FormattedMessage id={"header.komaxes_link"}/>,
          link : "/komaxes"
        },
    ].filter(page => {
        let link = page.link.toString().substr(1);
        if (props.role === "") return true;
        return link === "" || availablePages.includes(link);
    }).map((elem) => {
        let icon = undefined;
        switch (elem.link) {
            case "/": {
                icon = <Home/>;
                break;
            };
            case "/harnesses":{
                icon = <Folder/>;
                break;
            };
            case "/labour":{
                icon = <Clock/>;
                break;
            };
            case "/tasks":{
                icon = <Briefcase/>;
                break;
            };
            case "/terminals":{
                icon = <GitCommit/>;
                break;
            };
            case "/komaxes":{
                icon = <Settings/>;
                break;
            };
            default : {
                icon = <Settings/>;
                break;
            }
        }
        elem['icon'] = icon;
        return elem;
    });
    let [isOpen, setOpen] = useState(false);
    let toggleDrawer = (e) => {
        setOpen(!isOpen);
    }
    let close = (e) => {
        setOpen(false)
    }
    let renderedLinkItems = buttonsState.map((elem, index) => {
        return(
            <NavLink to={elem.link} className={classes.link} key={index} activeClassName={classes.activeLink}>
                <ListItem button key={elem.desc} onClick={toggleDrawer}>
                    <ListItemIcon>
                        {elem.icon}
                    </ListItemIcon>
                    <ListItemText primary={elem.desc} />
                </ListItem>
            </NavLink>
        );
    });
      const drawer = (
        <div>
          <div className={classes.toolbar} />
          <List>
              {renderedLinkItems}
          </List>
        </div>
      );
    return(
        <>
            <Drawer
                ModalProps={{
                  keepMounted: false, // Better open performance on mobile.
                }}
                anchor={"left"}
                open={isOpen}
                onClose={close}
            >
                {drawer}
            </Drawer>
            <div className={classes.Header}>
                <div className={classes.container}>
                    {props.isLogged
                        ?   <IconButton aria-label="delete" onMouseEnter={toggleDrawer} onClick={toggleDrawer}>
                                <MenuIcon/>
                            </IconButton>
                        :   <Redirect to={"/login"}/>
                    }
                    <div className={classes.logoWrapper}>
                        <img src={logo} alt={"logo"} className={classes.logo}/>
                    </div>
                    <button onClick={props.toggleLocale} className={classes.localeBtn}>
                        <FormattedMessage id={"header.locale_label"}/>
                    </button>
                    {props.isLogged
                        ? <button className={classes.logoutBtn} onClick={props.logout}>
                                <FormattedMessage id={"login.log_out_label"}/>
                          </button>
                        : <Redirect to={"/login"}/>
                    }
                </div>
            </div>
            <div className={classes.spacing}/>
        </>
    )
}

export default Header;