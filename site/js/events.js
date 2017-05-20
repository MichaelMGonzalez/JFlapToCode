function register_events() {
   network.on("selectEdge", function (params) {
        console.log('selectEdge Event:', params);
        var nodes = params.nodes;
        if(nodes.length == 0 ) {
            activeEdge = params.edges[0];
            network.manipulation.editEdgeMode();
   } });
  network.on("click", function (params) {
        console.log('click Event:', params);
        var nodes = params.nodes;
        var edges = params.edges;
        var mode = network.manipulation.inMode;
        var isAdding = ( mode === "addNode" || mode === "addEdge");
        console.log(isAdding);
        console.log(noSelection);
        var noSelection = (nodes.length == 0 && edges.length == 0);
        if( !isAdding && noSelection ) {
            clearAll();
        }
    });
  network.on("doubleClick", function (params) {
        console.log('dbl click Event:', params);
        var nodes = params.nodes;
        var edges = params.edges;
        var noSelection = (nodes.length == 0 && edges.length == 0);
        if( nodes.length == 1 && activeNode == nodes[0] ) {
            console.log("we got a winner");
            network.focus(activeNode);
        }
        //params.event = "[original event]";
    });
    document.onkeydown = function ( event ) {
        var key = event.keyCode;
        var use_shortcuts = prefix === empty_prefix;
        console.log(key);
        switch(event.keyCode) {
            case 27: // escape
                clearAll();
                break;
        }
        if(use_shortcuts) {
            switch(event.keyCode) {
                case 65: // aLinkcolor
                    network.manipulation.addNodeMode();
                    break;
                case 69: // e
                    network.manipulation.addEdgeMode();
                    break;
                case 83: // s
                    exportNetwork();
                    break;
                case 79: // s
                    loadNetwork();
                    break;
            }
        }
    }
}