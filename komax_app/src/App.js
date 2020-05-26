import React from 'react';
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

library.add(fas, fab);

let App = (props) => {
    return (
        <main>
          <BrowserRouter basename={process.env.PUBLIC_URL}>
              <Provider store={store}>
                  <Header/>
                  <Route path={"/"} exact>
                      Главная
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
    );
}

export default App;
