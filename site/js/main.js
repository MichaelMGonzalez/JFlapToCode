var nodes = { };
var edges = { };
var network = null;
var activeNode = null;
var activeEdge = null;
var file_loader = null;
var initial_node = null;

var node_prefix = "node";
var edge_prefix = "edge";

var container;
var new_prefix = "new";
var sidebar_prefix = "sidebar";
var empty_prefix = "";

var prefix = empty_prefix
// randomly create some nodes and edges
var data = getScaleFreeNetwork(0);
var seed = 2;

function destroy() {
  if (network !== null) {
    network.destroy();
    network = null;
  }
}

function draw() {
  destroy();
  // create a network
  container = document.getElementById('mynetwork');
  var options = {
    layout: {
        randomSeed:seed,
        hierarchical: {
                        sortMethod : "directed",
                        direction: "UD"
                    }

    }, 
    physics : {
        maxVelocity : 5,
        enabled : false,
        repulsion : {
                springLength : 300,
                nodeDistance : 500,
                springConstant : 1,
                damping : .3
        }
    },
    edges: {
          smooth: true
    },
    manipulation: {
      addNode: function (data, callback) {
        // filling in the popup DOM elements
        //document.getElementById('node-operation').innerHTML = "Add Node";
        document.getElementById('popup_header').innerHTML = "Add Node";
        enterEditMode(data, callback, new_prefix, saveNodeData);
      },
      editNode: function (data, callback) {
        // filling in the popup DOM elements
        document.getElementById('sidebar-operation').innerHTML = "Edit Node";
        editSidebar(data, callback, node_prefix);
      },
      addEdge: function (data, callback) {
        if (data.from == data.to) {
          var r = confirm("Do you want to connect the node to itself?");
          if (r != true) {
            callback(null);
            return;
          }
        }
        document.getElementById('popup_header').innerHTML = "Add Edge";
        enterEditMode(data, callback, new_prefix, saveEdgeData);
      },
      editEdge: {
        editWithoutDrag: function(data, callback) {
          document.getElementById('sidebar-operation').innerHTML = "Edit Edge";
          editSidebar(data,callback,edge_prefix);
        }
      },
      deleteNode : function(node, callback){
          console.log(node.id);
          delete data.nodes[ node.id ];
          callback(node);
          
      },
      deleteEdge: function( edge, callback ) {
          delete data.edges[ edge.id ];
          callback(edge);
      },
      initiallyActive: true,

    }
  };
  network = new vis.Network(container, data, options);
}

function editSidebar( data, callback, mode ) {
    var f, them;
    if( mode === edge_prefix ) {
        them = node_prefix;
        f = saveEdgeData;
    }
    else{
        them = edge_prefix;
        f = saveNodeData;
    }
    enterEditMode( data, callback, sidebar_prefix, f);
    var extras = document.getElementById(mode+'-options');
    var others = document.getElementById(them+'-options');
    extras.style.display = "block";
    others.style.display = "none";
}

function enterEditMode(data, callback, _prefix, save_function) {
  prefix = _prefix;
  switch( prefix ) {
      case new_prefix:
        clearSidebarPopUp();
        break;
      case sidebar_prefix:
        clearNewPopUp();
        break;
  }
  var label = document.getElementById(prefix + '-label');
  var f = save_function.bind(this, data, callback);
  var is_bad_name = data.label == null || data.label == "new";
  label.value = is_bad_name ? "" : data.label;
  label.onkeydown = function(event) {
      switch(event.keyCode) {
          case 13: //enter
          f();
          break;
      }
  }
  setTimeout( function() { label.focus();}, 10 );
  document.getElementById(prefix + '-saveButton').onclick = f;
  document.getElementById(prefix + '-popUp').style.display = 'block';
}


function clearAll() {
    network.manipulation.enableEditMode();
    clearSidebarPopUp();
    clearNewPopUp();
    prefix = "";
}

function clearNewPopUp() {
  document.getElementById(new_prefix + '-saveButton').onclick = null;
  document.getElementById(new_prefix + '-popUp').style.display = 'none';
}

function clearSidebarPopUp() {
  document.getElementById(sidebar_prefix + '-saveButton').onclick = null;
  document.getElementById(sidebar_prefix + '-popUp').style.display = 'none';
}

function saveNodeData(data, callback) {
  data.label = document.getElementById(prefix + '-label').value;
  initial_box = document.getElementById("initial_state");
  initial = initial_box.checked;
  initial_box.checked = false;
  if(initial && initial_node) {
    initial_node.initial = false;
    stylize_node(initial_node);
  }
  data.initial = initial;
  stylize_node(data);
  console.log(callback);
  initial_node = data;
  console.log(data);
  setTimeout( function() {
    nodes[ data.id ] = data;
    console.log( nodes );
    clearAll();
  }, 1);
  callback(data);
}

function saveEdgeData(data, callback) {
  if (typeof data.to === 'object')
    data.to = data.to.id
  if (typeof data.from === 'object')
    data.from = data.from.id
  data.label = document.getElementById(prefix + '-label').value;
  data.arrows = { "to" : true };
  data.length = 15;
  console.log( data );
  callback(data);
  setTimeout( function() {
    edges[ data.id ] = data;
    console.log( edges );
    clearAll();
  }, 1);
}

function delete_selected() {
    var graph = network.getSelection();
    deleteAll( edges, graph.edges );
    deleteAll( nodes, graph.nodes );
    network.deleteSelected();
}

function deleteAll( container, values ) {
    for( var i = 0; i < values.length; i++ ) {
        delete container[ values[i] ];
    }
}


function readSingleFile(e, onload) {
  var file = e.target.files[0];
  if (!file) {
    return;
  }
  var reader = new FileReader();
  reader.onload = function(e) {
    var contents = e.target.result;
    onload(file_loader.value, contents);
  };
  reader.readAsText(file);
}

function readUserInput( e) {
    readSingleFile( e, importNetwork );
}

function importNetwork(name, s) {
    s = s.replace(/\\n/g, "\\n")  
               .replace(/\\'/g, "\\'")
               .replace(/\\"/g, '\\"')
               .replace(/\\&/g, "\\&")
               .replace(/\\r/g, "\\r")
               .replace(/\\t/g, "\\t")
               .replace(/\\b/g, "\\b")
               .replace(/\\f/g, "\\f");
    // remove non-printable and other non-valid JSON chars
    s = s.replace(/[\u0000-\u0019]+/g,""); 
    console.log(s);
    var inputData = JSON.parse(s);
    var _nodes = inputData.nodes;
    var _edges = inputData.edges;
    _nodes.forEach( load_node );
    _edges.forEach( load_edge );
    data = {
        nodes: _nodes,
        edges: _edges
    }
    network.setData(data);

}

function getNetworkJSON ( ) {
    var _nodes = objectToArray( nodes );
    var _edges = objectToArray( edges );
    
     
    var graph = { "nodes" : _nodes, "edges": _edges };

    // pretty print node data
    var exportValue = JSON.stringify(graph, undefined, 2);
    console.log(exportValue);
    return exportValue;
}

function exportNetwork() {
    var exportValue = getNetworkJSON();
    var blob = new Blob([exportValue], {type: "text/plain;charset=utf-8"});
    saveAs(blob, "not_jflap.fsm");
}


function load_node( node ) {
    stylize_node(node);
    nodes[ node.id ] = node;
}
function load_edge( edge ) {
    edges[ edge.id ] = edge;
}
function stylize_node( node ) {
    if(node) {
        if(node.initial) {
          node.shape = 'triangleDown';
          node.color = "#f4f442";
        }
        else {
          node.initial = false;
          node.shape = 'ellipse';
          node.color = "#a4b8db";
        }
    }
}

function loadNetwork() {
    loader.click();
}

function objectToArray(obj) {
    return Object.keys(obj).map(function (key) { return obj[key]; });
}
function init() {
    file_loader = document.getElementById('loader');
    file_loader.addEventListener('change', readUserInput, false);
    draw();
      network.on("selectNode", function (params) {
        console.log('selectNode Event:', params);
        activeNode = params.nodes[0];
        network.manipulation.editNode();
    });
    register_events();
    try {
        importNetwork( "", document.cookie );
    }
    catch( e ) {
    }
}

function auto_save( ) {
    var d = getNetworkJSON( );
    document.cookie = d;
}
