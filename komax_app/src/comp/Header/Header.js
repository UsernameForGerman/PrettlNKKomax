import classes from "./Header.module.css"
import React, {useState} from "react";
import {NavLink} from "react-router-dom";
import logo from "../../assets/images/logo2.png"
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";

import MenuIcon from '@material-ui/icons/Menu';
import InboxIcon from "@material-ui/icons/Inbox"

import Drawer from "@material-ui/core/Drawer";
import List from "@material-ui/core/List";
import IconButton from "@material-ui/core/IconButton";
import ListItemIcon from "@material-ui/core/ListItemIcon";

import {Briefcase, Clock, Folder, GitCommit, Home, Settings} from "react-feather";

let Header = (props) => {
    let buttonsState = [
        {
          desc : "Start",
          link : "/"
        },
        {
          desc : "Tasks",
          link : "/tasks"
        },
        {
          desc : "Harnesses",
          link : "/harnesses"
        },
        {
          desc : "Komax terminals",
          link : "/terminals"
        },
        {
          desc : "Labor input",
          link : "/input"
        },
        {
          desc : "Komaxes",
          link : "/komaxes"
        }
    ].map((elem) => {
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
            case "/input":{
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
        }
        elem['icon'] = icon;
        return elem;
    });
    let [isOpen, setOpen] = useState(false);
    let toggleDrawer = () => {
        setOpen(!isOpen);
    }
    let renderedLinkItems = buttonsState.map((elem) => {
        return(
            <NavLink to={elem.link} className={classes.link} key={elem.desc} activeClassName={classes.activeLink}>
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
                open={isOpen}
                onClose={toggleDrawer}
            >
                {drawer}
            </Drawer>
            <div className={classes.Header}>
                <div className={classes.container}>
                    <IconButton aria-label="delete" onMouseEnter={toggleDrawer}>
                        <MenuIcon/>
                    </IconButton>
                    <div className={classes.logoWrapper}>
                        <img src={logo} alt={"logo"} className={classes.logo}/>
                    </div>
                </div>
            </div>
            <div className={classes.spacing}/>
        </>
    )
}

export default Header;