import {applyMiddleware, combineReducers, createStore} from "redux";
import {komaxReducer} from "./reducers/komaxReducer";
import thunk from "redux-thunk";
import {harnessesReducer} from "./reducers/harnessReducer";

const reducers = combineReducers({
    komaxes : komaxReducer,
    harnesses : harnessesReducer
});

const store = createStore(reducers, applyMiddleware(thunk));

export default store;