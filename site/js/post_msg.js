function post_network( dest, filetype ) {
    var full_dest = "/compile/" + dest;
    var msg = { "network" : getNetworkJSON() };
    var callback = function ( data ) {
        console.log( data );
        var blob = new Blob([data], {type: "text/plain;charset=utf-8"});
        saveAs(blob, "not_jflap" + filetype);
    };
    $.post( full_dest, msg, callback );
}