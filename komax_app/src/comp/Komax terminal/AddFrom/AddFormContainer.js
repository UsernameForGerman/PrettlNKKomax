import React, {useState} from "react";
import AddForm from "./AddForm";

let AddFormContainer = (props) => {
    let [materialValue, setMaterial] = useState("False");
    let [terminalAvaliable, setTerminal] = useState("False");
    return(
        <AddForm
            materialValue={materialValue}
            setMaterial={setMaterial}
            terminalAvaliable={terminalAvaliable}
            setTerminal={setTerminal}
        />
    )
}

export default AddFormContainer;