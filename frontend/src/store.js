import {applyMiddleware, combineReducers, createStore} from "redux";
import {komaxReducer} from "./reducers/komaxReducer";
import thunk from "redux-thunk";
import {harnessesReducer} from "./reducers/harnessesReducer";
import {authReducer} from "./reducers/authReducer";
import {modalReducer} from "./reducers/modalReducer";
import {komaxTerminalReducer} from "./reducers/komaxTerminalReducer";
import {labourReducer} from "./reducers/labourReducer";
import {tasksReducer} from "./reducers/tasksReducer";
import {kappasReducer} from "./reducers/kappasReducer";
import {sealReducer} from "./reducers/sealReducer";

const reducers = combineReducers({
    komaxes : komaxReducer,
    login : authReducer,
    harnesses : harnessesReducer,
    modal : modalReducer,
    terminals : komaxTerminalReducer,
    labour : labourReducer,
    tasks : tasksReducer,
    kappa : kappasReducer,
    seal : sealReducer
});

const store = createStore(reducers, applyMiddleware(thunk));

export default store;