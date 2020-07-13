import React from "react";
import {FormattedMessage} from "react-intl";

let getStatus = (num) => {
    switch (num) {
        case 1 : return <FormattedMessage id={"working_status"}/>;
        case 2 : return <FormattedMessage id={"repairing_status"}/>;
        case 3 : return <FormattedMessage id={"not_working_status"}/>;
        default : return num;
    }
}

let getMarking = (num) => {
    switch (num) {
        case 1 : return <FormattedMessage id={"black_marking"}/>;
        case 2 : return <FormattedMessage id={"white_marking"}/>;
        case 3 : return <FormattedMessage id={"both_marking"}/>;
        default : return num;
    }
}

let getSepairing = (num) => {
    switch (num) {
        case "1" : return "0.5 - 1.0";
        case "2" : return "1.5 - 2.5";
        case "3" : return "4.0 - 6.0";
        default : return num;
    }
}

export {getStatus, getMarking, getSepairing}