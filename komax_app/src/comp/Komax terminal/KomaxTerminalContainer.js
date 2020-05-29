import KomaxTerminal from "./KomaxTerminal";
import React, {useState} from "react";
import KomaxTerminalTableItem from "./KomaxTerminalTable/Item/KTTItem";
import createTerminal from "../../DAL/models/terminal";

let KomaxTerminalContainer = (props) => {
    let [selectedTerminal, setSelectedTerminal] = useState();
    const [materialValue, setMaterialValue] = useState();
    const [terminalAvaliable, setTerminalAvaliable] =useState();
    let items = [
        {
            terminal_number : "1060-16-0122",
            terminal_avaliable : "True",
            material_avaliable : "False"
        },
        {
            terminal_number : "1060-20-0122",
            terminal_avaliable : "True",
            material_avaliable : "False"
        },
        {
            terminal_number : "1062-12-0166",
            terminal_avaliable : "False",
            material_avaliable : "True"
        },
        {
            terminal_number : "1062-16-0122",
            terminal_avaliable : "True",
            material_avaliable : "True"
        }
    ].map((item) => {
        let select = () => {
            setSelectedTerminal(item);
            setMaterialValue(item.material_avaliable);
            setTerminalAvaliable(item.terminal_avaliable);
        }
        return (
            <KomaxTerminalTableItem {...item} select={select}/>
        )
    })

    return(

        <KomaxTerminal items={items}
                       selected={selectedTerminal}
                       setMaterial={setMaterialValue}
                       setTerminal={setTerminalAvaliable}
                       terminalAvaliable={terminalAvaliable}
                       materialValue={materialValue}
        />
    )
}

export default KomaxTerminalContainer;