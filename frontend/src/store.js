import {applyMiddleware, combineReducers, createStore} from "redux";
import {komaxReducer} from "./reducers/komaxReducer";
import thunk from "redux-thunk";
import {harnessesReducer} from "./reducers/harnessesReducer";
import {loginReducer} from "./reducers/loginReducer";
import {modalReducer} from "./reducers/modalReducer";
import {komaxTerminalReducer} from "./reducers/komaxTerminalReducer";
import {labourReducer} from "./reducers/labourReducer";
import {tasksReducer} from "./reducers/tasksReducer";
import {kappasReducer} from "./reducers/kappasReducer";

const reducers = combineReducers({
    komaxes : komaxReducer,
    login : loginReducer,
    harnesses : harnessesReducer,
    modal : modalReducer,
    terminals : komaxTerminalReducer,
    labour : labourReducer,
    tasks : tasksReducer,
    kappa : kappasReducer
});

const store = createStore(reducers, applyMiddleware(thunk));

export default store;