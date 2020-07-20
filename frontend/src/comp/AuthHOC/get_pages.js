let get_pages = (permission) => {
    let perm = permission === null ? "" : permission.toString().toLowerCase();
    switch (perm) {
        case "master" : {
            return ['account', 'tasks', 'task', 'task_create', 'komaxes', 'harnesses'];
        }

        case "archivarius" : {
            return ['account', 'harnesses']
        }

        case "mechanic" : {
            return ['account', 'komaxes']
        }

        case "operator" : {
            return ['account', 'tasks', 'task', 'task_create']
        }

        case "technologist" : {
            return ['account', 'terminals', 'labour', 'komaxes']
        }

        case "admin" : {
            return ['account', 'tasks', 'task', 'task_create', 'harnesses', 'terminals', 'labour', 'komaxes']
        }

        default : {
            return ['account']
        }
    }
}

export default get_pages;