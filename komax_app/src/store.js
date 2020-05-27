import {applyMiddleware, combineReducers, createStore} from "redux";
import {komaxReducer} from "./reducers/komaxReducer";
import thunk from "redux-thunk";
import {harnessesReducer} from "./reducers/harnessReducer";
import {loginReducer} from "./reducers/loginReducer";

const reducers = combineReducers({
    komaxes : komaxReducer,
    login : loginReducer,
    harnesses : harnessesReducer
});

const store = createStore(reducers, applyMiddleware(thunk));

export default store;