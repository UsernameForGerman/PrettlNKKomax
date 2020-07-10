let format = (time, locale) => {
    let obj = {
        sec : time,
        min : 0,
        h : 0,
        d : 0
    }

    let keys = Object.keys(obj);
    keys.forEach((elem, index) => {
        let curr = obj[elem];
        let mod = index === 2 ? 24 : 60;
        let next = Math.floor(curr / mod);
        if (index < 3){
            obj[elem] = curr % mod;
            obj[keys[index + 1]] += next;
        }
    })

    let str = "";
    keys.forEach((elem, index) => {
        let key = keys[keys.length - 1 - index];
        let value = obj[key];
        debugger;
        switch (key) {
            case "sec" : {
                str += value > 0 ? value + (locale === "ru" ? "сек" : key) : ""
                break;
            }

            case "min" : {
                str += value > 0 ? value + (locale === "ru" ? "мин" : key) : ""
                break;
            }

            case "h" : {
                str += value > 0 ? value + (locale === "ru" ? "ч" : key) : ""
                break;
            }

            case "d" : {
                str += value > 0 ? value + (locale === "ru" ? "д" : key) : ""
                break;
            }
        }
        str +=  " ";
    })

    return str;
}

export default format;