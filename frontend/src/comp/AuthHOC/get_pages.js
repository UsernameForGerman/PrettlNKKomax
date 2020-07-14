let get_pages = (permission) => {
    switch (permission) {
        case "Master" : {
            return ['account', 'tasks', 'task', 'task_create', 'komaxes', 'harnesses'];
        }

        case "Archivarius" : {
            return ['account', 'harnesses']
        }

        case "Mechanic" : {
            return ['account', 'komaxes']
        }

        case "Operator" : {
            return ['account', 'tasks', 'task', 'task_create']
        }

        case "Technologist" : {
            return ['account', 'terminals', 'labour', 'komaxes']
        }

        case "Admin" : {
            return ['account', 'tasks', 'task', 'task_create', 'harnesses', 'terminals', 'labour', 'komaxes']
        }
    }
}

export default get_pages;