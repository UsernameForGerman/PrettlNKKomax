import React, {useState} from 'react';
import {BrowserRouter, Redirect, Route} from "react-router-dom";
import "./Global.css";
import {Provider} from "react-redux";
import store from "./store";
import KomaxesContainer from "./comp/Komaxes/KomaxesContainer";
import HarsessesContainer from "./comp/Harnesses/HarnessesContainer";
import { fab } from '@fortawesome/free-brands-svg-icons'
import { fas } from '@fortawesome/free-solid-svg-icons'
import {library} from "@fortawesome/fontawesome-svg-core";
import LoginContainer from "./comp/Login/LoginContainer";
import KomaxTerminalContainer from "./comp/Komax terminal/KomaxTerminalContainer";
import messages_ru from "./localization/ru.json";
import messages_en from "./localization/en.json";
import {IntlProvider} from "react-intl";
import StartPageContainer from "./comp/Start/StartPageContainer";
import TasksPageContainer from "./comp/Tasks/TasksPageContainer";
import CreateTaskPageContainer from "./comp/Tasks/CreateTaskPage/CreateTaskPageContainer";
import TaskDetailPageContainer from "./comp/Tasks/TaskDetailPage/TaskDetailPageContainer";
import LabourPageContainer from "./comp/Labour/LabourPageContainer";
import HeaderContainer from "./comp/Header/HeaderContainer";
import './index.css'
import LandingPage from "./comp/LandingPage/LandingPage";
library.add(fas, fab);

let App = (props) => {
    const messages = {
        'ru': messages_ru,
        'en': messages_en
    };
    let [locale, setLocale] = useState('ru');
    let toggleLocale = () => {
        if (locale === 'ru'){
            setLocale('en');
        } else {
            setLocale('ru');
        }
    }
    return (
        <IntlProvider locale={locale} messages={messages[locale]}>
            <main>
              <BrowserRouter basename={process.env.PUBLIC_URL}>
                  <Provider store={store}>
                      <HeaderContainer toggleLocale={toggleLocale}/>
                      <Route path={"/api/"} exact>
                          <Redirect to={"/"}/>
                      </Route>
                      <Route path={"/static/komax_app"} exact>
                          <Redirect to={"/"}/>
                      </Route>
                      <Route path={"/labour"} exact>
                          <LabourPageContainer/>
                      </Route>
                      <Route path={"/tasks"} exact>
                          <TasksPageContainer/>
                      </Route>
                      <Route path={"/task_create"} exact>
                          <CreateTaskPageContainer/>
                      </Route>
                      <Route path={"/task/:id?"}>
                          <TaskDetailPageContainer locale={locale}/>
                      </Route>
                      <Route path={"/account"} exact>
                          <StartPageContainer/>
                      </Route>
                      <Route path={"/login"} exact>
                          <LoginContainer/>
                      </Route>
                      <Route path={"/terminals"} exact>
                          <KomaxTerminalContainer/>
                      </Route>
                      <Route path={"/komaxes"} exact>
                          <KomaxesContainer/>
                      </Route>
                      <Route path={"/harnesses"} exact>
                          <HarsessesContainer/>
                      </Route>
                  </Provider>
              </BrowserRouter>
            </main>
        </IntlProvider>
    );
}

export default App;
