import React from "react";
import classes from "./DescSection.module.css"

let DescSection = (props) => {
    return (<section className={classes.desc_section}>
                <div className={classes.desc_heading}>
                    <div className={classes.desc_heading_row}>
                        Управляй
                    </div>
                    <div className={classes.desc_heading_row}>
                        Быстрее. Дешевле. Стабильнее
                    </div>
                    <div className={classes.desc_heading_bottom}>
                         с автоматизацией и оцифровкой производственных процессов с TetraD-NK
                    </div>
                </div>
                <div className={classes.desc_btns}>
                    <button className={classes.desc_btn}>
                        Создать
                    </button>
                    <button className={classes.desc_btn}>
                        Обсудить проект
                    </button>
                </div>
            </section>)
}

export default DescSection;