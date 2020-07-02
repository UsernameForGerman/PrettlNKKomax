let get_pages = (permission) => {
    switch (permission) {
        case "Master" : {
            return ['tasks', 'task', 'task_create', 'komaxes', 'harnesses'];
        }

        case "Archivarius" : {
            return ['harnesses']
        }

        case "Mechanic" : {
            return ['komaxes']
        }

        case "Operator" : {
            return ['tasks', 'task', 'task_create']
        }

        case "Technologist" : {
            return ['terminals', 'labour', 'komaxes']
        }

        case "Admin" : {
            return ['tasks', 'task', 'task_create', 'harnesses', 'terminals', 'labour', 'komaxes']
        }
    }
}

export default get_pages;