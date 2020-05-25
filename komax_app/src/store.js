import {applyMiddleware, combineReducers, createStore} from "redux";
import {komaxReducer} from "./reducers/komaxReducer";
import thunk from "redux-thunk";

const reducers = combineReducers({
    komaxes : komaxReducer
});

const store = createStore(reducers, applyMiddleware(thunk));

export default store;