


function socket_adress(location){
    var loc = location;

    var wsStart = 'ws://'

    if (loc.protocol == 'https'){
        wsStart = 'wss://'
    }

    return wsStart + loc.host + loc.pathname;
}