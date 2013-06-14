/**
 * editor_plugin_src.js
 *
 * Copyright 2009, Moxiecode Systems AB
 * Released under LGPL License.
 *
 * License: http://tinymce.moxiecode.com/license
 * Contributing: http://tinymce.moxiecode.com/contributing
 */

tinyMCE.addI18n(
    {da : {divwrap : {
	"title" : "Pak det valgte ind",
	"none_title" : "Ingen indpakning",
	"factBox_title" : "Faktaboks",
    "linkButton_title" : "Link knap"
    }}}
);
tinyMCE.addI18n(
    {en : {divwrap : {
	"title" : "Wrap selected content",
	"none_title" : "Do not wrap",
	"factBox_title" : "Factbox",
    "linkButton_title" : "Linkbutton"
    }}}
);

var wrapper_classes = ['none',
		       'factBox',
               'linkButton'
		      ];

(function() {
    tinymce.create('tinymce.plugins.DivWrapPlugin', {

	init : function(ed, url) {

	    this.url = url;
	    ed.onInit.add(function(ed) {
		for(var i=0; i<wrapper_classes.length; i++) {
		    ed.formatter.register(wrapper_classes[i], {"block" : "div", "classes" : wrapper_classes[i], "wrapper" : "true"});
		}
	    });
	    
	    ed.addCommand('exclusiveApplyFormat', function(format) {
		var applied_formats = ed.formatter.matchAll(wrapper_classes);
		for(var i=0; i<applied_formats.length; i++) {
		    ed.formatter.remove(applied_formats[i]);
		}
		if (format != 'none') {
		    ed.formatter.apply(format);
		}
	    });
	},
	
        createControl: function(n, cm) {
            switch (n) {
            case 'divwrap':
                var c = cm.createMenuButton('divwrap', {
                    title : 'divwrap.title',
                    image : this.url + '/img/box.png',
                    icons : false
                });
                c.onRenderMenu.add(function(c, m) {
		    for(var i=0; i<wrapper_classes.length; i++) {
			function addMenu(format) {
			    m.add({title : 'divwrap.'+format+'_title', onclick : function() {
				tinyMCE.activeEditor.execCommand('exclusiveApplyFormat', format);
			    }});
			};
			addMenu(wrapper_classes[i]);
		    }
                });
                // Return the new menu button instance
                return c;
            }
            return null;
        }
});

	// Register plugin
	tinymce.PluginManager.add('divwrap', tinymce.plugins.DivWrapPlugin);
})(); 
