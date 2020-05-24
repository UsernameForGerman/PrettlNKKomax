import React from 'react';
import {BrowserRouter} from "react-router-dom";
import Header from "./comp/Header/Header";
import Komaxes from "./comp/Komaxes/Komaxes";
import "./Global.css";
import {Provider} from "react-redux";
import store from "./store";
import KomaxesContainer from "./comp/Komaxes/KomaxesContainer";

let App = (props) => {
    return (
        <main>
          <BrowserRouter basename={process.env.PUBLIC_URL}>
              <Provider store={store}>
                <Header/>
                <KomaxesContainer/>
              </Provider>
          </BrowserRouter>
        </main>
    );
}

export default App;
