odoo.define('web_gantt_native.HeaderHint', function (require) {
"use strict";


var core = require('web.core');
var Widget = require('web.Widget');
var time = require('web.time');

var _t = core._t;



var GanttHeaderHint = Widget.extend({
    template: "GanttHeaderHint",


    init: function(parent) {

        this._super(parent);

    },

    start: function() {

        var self = this;

        self.$el.append('<div class="task-gantt-line-hint-names"></div>');
        $('<div class="task-gantt-line-hint-name"></div>').appendTo(self.$el.children(".task-gantt-line-hint-names"));

        self.$el.append('<div class="task-gantt-line-hint-values"></div>');
        $('<div class=hint-start-value class="task-gantt-line-hint-value"></div>').appendTo(self.$el.children(".task-gantt-line-hint-values"));

    },


    renderElement: function () {
        this._super();

    },

    show_hint : function(target, ex, ey) {

        var self = this;

        var o_left = ex;
        var o_top = ey;

        this.$el.find('div.hint-start-value').text(target['data-id']);
        this.$el.offset({ top: o_top+30, left: o_left});

    }

});

return GanttHeaderHint;

});