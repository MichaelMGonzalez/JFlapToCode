var State = fabric.util.createClass( fabric.Circle, {
    type: "StateNode",
    initialize : function( options ) {
        options.radius = 35;
        this.callSuper('initialize', options);
    }
} );

// Context Menu jazz

var c_btn_w = 175;
var c_btn_h = 40;

var ContextMenu = fabric.util.createClass( fabric.Rect, {
    type: "ContextMenu",
    buttons : [],
    hide : function() {
        this._anim('.0');
    },
    show : function(loc) {
        this.left = loc.left;
        this.top  = loc.top;
        this._anim('.8');
    },
    _anim: function(opacity) {
        this.animate('opacity', opacity, {
            duration: 200,
            onChange: canvas.renderAll.bind(canvas),
        });
    },
    initialize : function( options ) {
        options.width  = 200;
        options.height = 150;
        options.top  = ( options.top - options.height > 0 ? options.top : options.height/2);
        options.left = ( options.left - options.height > 0 ? options.left : options.width/2);
        options.fill   = 'rgba(127,127,127, .8)';
        options.selectable = false;
        this.callSuper('initialize', options);
    }
} );

var ContextMenuButton = fabric.util.createClass( fabric.Rect, {
    type: "ContextMenuBtn",
    initialize : function( options ) {
        options.width  = c_btn_w;
        options.height = c_btn_h;
        options.selectable = false;
        this.callSuper('initialize', options);
    }
} );
