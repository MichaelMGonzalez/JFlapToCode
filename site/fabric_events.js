var canvas = this.__canvas = new fabric.Canvas('c90');
(function() {

  canvas.on({
    'mouse:down' : onLeftClick 
  });  

  var contextMenu = new ContextMenu({});
  canvas.add(contextMenu);
  contextMenu.hide();

  function onLeftClick(fabricEvent) {
        var t = fabricEvent.target;
        if( t === null ) {
            spawnState(fabricEvent.e);
            deactivateContextMenu();
        }
        if( t !== null )
            console.log(t.name);
  }

  function onRightClick(jsEvent, fabricObject) {
      switch(fabricObject) {
          case null:
              spawnContextMenu( jsEvent );
              break;
          default:
              console.log("Default case!");
              break;
      }
  }

  function spawnState( jsEvent ) {
    var circle = new State( getPoint(jsEvent) );
    canvas.add(circle);
  }

  function spawnContextMenu( jsEvent ) {
    deactivateContextMenu();
    contextMenu.show( getPoint( jsEvent ));
  }

  function deactivateContextMenu( ) {
    if( contextMenu ) {
        contextMenu.hide();
        //canvas.remove( contextMenu );
        //contextMenu = null;
    }
  }

  function getPoint(jsEvent) {
    var clickPoint = new fabric.Point(jsEvent.offsetX, jsEvent.offsetY);
    var x = clickPoint.x;
    var y = clickPoint.y;
    var params = {left : x, top : y};
    return params;
  }
 
  // Use jquery to unbind default context menu
  // Enables custom right click events
  $('.upper-canvas').bind('contextmenu', function (e) {
      var objectFound = false;
      var clickPoint = new fabric.Point(e.offsetX, e.offsetY);
      var fabricObject = null;
      e.preventDefault();
      // Iterate over all objects to find where we clicked
      canvas.forEachObject(function (obj) {
          if (!fabricObject && obj.containsPoint(clickPoint)) {
              fabricObject = obj;
          }
      });
      // Fire event
      onRightClick( e, fabricObject );
  });

})();
