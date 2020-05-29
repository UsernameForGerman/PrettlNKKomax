import React, {useState} from 'react';
import {BrowserRouter, Route} from "react-router-dom";
import Header from "./comp/Header/Header";
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
                      <Header toggleLocale={toggleLocale}/>
                      <Route path={"/"} exact>
                          Главная страница
                      </Route>
                      <Route path={"/login"}>
                          <LoginContainer/>
                      </Route>
                      <Route path={"/terminals"}>
                          <KomaxTerminalContainer/>
                      </Route>
                      <Route path={"/komaxes"}>
                          <KomaxesContainer/>
                      </Route>
                      <Route path={"/harnesses"}>
                          <HarsessesContainer/>
                      </Route>
                  </Provider>
              </BrowserRouter>
            </main>
        </IntlProvider>
    );
}

export default App;
