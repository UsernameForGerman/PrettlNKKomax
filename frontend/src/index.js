import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import * as serviceWorker from './serviceWorker';
import './index.css';
import 'antd/dist/antd.css';
import LandingPage from "./comp/LandingPage/LandingPage";

let pathname = window.location.pathname;
let index = pathname.toString().substr(1).indexOf('/');
let path = window.location.pathname.toString().substr(1, index > 0 ? index : pathname.length);
ReactDOM.render(
    <>
        {path === ''
            ? <LandingPage/>
            : <App />
        }
    </>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
