odoo.define('web_gantt_native.ItemOptions', function (require) {
"use strict";

var Widget = require('web.Widget');
var Model = require('web.AbstractModel');
var framework = require('web.framework');

var dialogs = require('web.view_dialogs');
var core = require('web.core');
var _t = core._t;
var _lt = core._lt;

var time = require('web.time');

var GanttListOptionsItem = Widget.extend({
    template: "GanttList.options",

    custom_events: {
        'item_order' : 'order_action',
        'item_list' : 'list_action',
        'item_export' : 'export_action',
        'item_industry' : 'industry_action',
        'item_week' : 'week_action'

    },

    init: function(parent) {
        this.parent = parent;
        this._super.apply(this, arguments);
        this.$zTree = parent.widget_ztree.$zTree;
    },

    start: function () {
        // var _widget =  this.parent.gantt_timeline_header_widget;
        // var el_widget = _widget.$el;

        if (this.parent.ItemsSorted){

            // var div_manual = $('<div class="text-left task-gantt-item-sort-manual"/>');
            // div_manual.text("Manual Sort");
            // this.$el.append(div_manual);

        } else if (this.parent.state.orderedBy && this.parent.state.orderedBy.length){

            // Sort Options
            var div_ = $('<div class="text-left gantt-list-options-item"/>');
            // div_.text(this.parent.fields[this.parent.state.orderedBy[0].name].string);
            var _text = "Sort - " + this.parent.fields[this.parent.state.orderedBy[0].name].string;

            var  div_typer = $('<div class="fa fa-sort-amount-desc gantt-list-options-item-sort" aria-hidden="false" title="desc '+ _text +'"></div>');


            if (this.parent.state.orderedBy[0].asc){
                 div_typer = $('<div class="fa fa-sort-amount-asc gantt-list-options-item-sort" aria-hidden="false" title="asc '+ _text +'"></div>');
            }

            div_.append(div_typer);
            this.$el.append(div_);

        }

        // Show List -basic, -active, -inactive

        var item_list = $('<div class="text-left gantt-list-options-item"/>');

        var list_div = $('<div class="fa fa-list gantt-list-options-item-check gantt-list-options-item-check-basic" data-key="basic" aria-hidden="false" title="Show Basic"></div>');

        if (this.parent.list_show === 1){
            list_div = $('<div class="fa fa-list gantt-list-options-item-check gantt-list-options-item-check-active" data-key="active" aria-hidden="false" title="Show All"></div>');
        }
        else if (this.parent.list_show === -1){
            list_div = $('<div class="fa fa-list gantt-list-options-item-check gantt-list-options-item-check-inactive" data-key="inactive" aria-hidden="false" title="Show Disable"></div>');
        }

        item_list.append(list_div);
        this.$el.append(item_list);


        //Export to file

        var export_to_file = $('<div class="text-left gantt-list-options-item"/>');
        var export_to_file_div = $('<div class="fa fa-file-text-o gantt-list-options-export-to-file" aria-hidden="false" title="Screen to PDF"></div>');

        export_to_file.append(export_to_file_div);
        this.$el.append(export_to_file);


        // Time line for Industry
        var industry_to_file = $('<div class="text-left gantt-list-options-item"/>');
        var industry_to_file_div = $('<div class="fa fa-industry gantt-list-options-industry gantt-list-options-industry-hide " data-key="hide" aria-hidden="false" title="Time Line"></div>');
        if (this.parent.industry_show === 1){
            industry_to_file_div = $('<div class="fa fa-industry gantt-list-options-industry gantt-list-options-industry-show" data-key="show" aria-hidden="false" title="Time Line"></div>');
        }

        industry_to_file.append(industry_to_file_div);
        this.$el.append(industry_to_file);

        //IsoWeek

        var week_icon = $('<div class="text-left gantt-list-options-item"/>');
        var week_icon_div = $('<div class="fa fa-building gantt-list-options-week gantt-list-options-week-isoweek " data-key="isoweek" aria-hidden="false" title="Iso Week"></div>');
        if (this.parent.week_type === "week"){
            week_icon_div = $('<div class="fa fa-building gantt-list-options-week gantt-list-options-week-week" data-key="week" aria-hidden="false" title="Week"></div>');
        }

        week_icon.append(week_icon_div);
        this.$el.append(week_icon);


    },


    renderElement: function () {
        this._super();

        this.$el.data('parent', this);
        this.$el.on('click', this.proxy('on_global_click'));

    },

    on_global_click: function (ev) {

        if (!ev.isTrigger) { //human detect

            if ($(ev.target).hasClass("gantt-list-options-item-sort" )) {

                this.trigger_up('item_order', {
                    orderedBy: this.parent.state.orderedBy,
                });
            }

            else if ($(ev.target).hasClass("gantt-list-options-item-check" )) {
                this.trigger_up('item_list', {"key": ev.target.dataset.key});
            }

            else if ($(ev.target).hasClass("gantt-list-options-export-to-file" ))
            {
                this.trigger_up('item_export', {});
            }
            else if ($(ev.target).hasClass("gantt-list-options-industry" )) {
                this.trigger_up('item_industry', {"key": ev.target.dataset.key});
            }
            else if ($(ev.target).hasClass("gantt-list-options-week" )) {
                this.trigger_up('item_week', {"key": ev.target.dataset.key});
            }

        }
    },

    order_action: function(event) {

        var self = this.__parentedParent;
        var parent = this.parent;
        var orderedBy = event.data.orderedBy;


        if (orderedBy.length){

            if (orderedBy[0].asc){
                orderedBy[0].asc = false
            }else{

                orderedBy[0].asc = true
            }

            self.trigger_up('gantt_refresh_after_change' )

        }
    },

    list_action: function(event) {

        var self = this.__parentedParent;
        var parent = this.parent;

        var e_key = event.data.key;
        let list_show = 0
        // basic, active, inactive
        if (e_key === "active") {
            list_show = -1
        } else if (e_key === "inactive") {
            list_show = 0
        } else if (e_key === "basic") {
            list_show = 1
        }

        parent.list_show = list_show
        parent.local_storage.setItem("gantt_list_show", list_show)

        self.trigger_up('gantt_fast_refresh_after_change' )

    },

    industry_action: function(event) {

        var self = this.__parentedParent;
        var parent = this.parent;

        var e_key = event.data.key;
        let industry_show = 0
        // basic, active, inactive
        if (e_key === "hide") {
            industry_show = 1
        }

        parent.industry_show = industry_show
        parent.local_storage.setItem("gantt_industry_show", industry_show)

        self.trigger_up('gantt_fast_refresh_after_change' )

    },

    week_action: function(event) {

        var self = this.__parentedParent;
        var parent = this.parent;

        var e_key = event.data.key;
        let week_type = "week"
        // basic, active, inactive
        if (e_key === "week") {
            week_type = "isoweek"
        }

        parent.week_type = week_type
        parent.local_storage.setItem("gantt_week_type", week_type)

        self.trigger_up('gantt_fast_refresh_after_change' )

    },




    export_action: function(event) {

        var self = this;
        var parent_app = this.__parentedParent;
        var parent = this.parent;


        var zTree = this.$zTree;
        //
        var nodes = zTree.getNodes();


        var rows_to_gantt = [];

        _.each(nodes, function (node) {

            var childNodes = zTree.transformToArray(node);

            _.each(childNodes, function (row) {



                var date_start = undefined;
                if (typeof row.task_start !== "undefined" ){
                    date_start = time.auto_date_to_str(row.task_start, "datetime")
                }

                var date_end = undefined;
                if (typeof row.task_stop !== "undefined" ){
                    date_end = time.auto_date_to_str(row.task_stop, "datetime")
                }


                var subtask_count = 0;
                if (row.isParent){
                        subtask_count = 1
                    }

                var for_update = {
                        "id": row.id,
                        "name": row.value_name,
                        "duration": row.duration,
                        "date_start": date_start,
                        "date_end": date_end,
                        "sorting_level": row.level,
                        "subtask_count": subtask_count,
                        "wbs": undefined,
                        "stuff": "",
                        "separate": row.is_group

                };
                rows_to_gantt.push(for_update)

            });

        });

        var pre_data = []

        _.each(parent_app.Predecessor, function (predecessor) {

            var pre_update = {

                "task_id": predecessor.task_id[0],
                "parent_task_id": predecessor.parent_task_id[0],
                "type": predecessor.type
            }
            pre_data.push(pre_update)

        })


        var context = this.__parentedParent.state.contexts;

        context['time_type'] = parent_app.timeType || false;
        context['default_screen'] = true;
        context['default_data_json'] = JSON.stringify(rows_to_gantt);
        context['default_pre_json'] = JSON.stringify(pre_data);



        var res_model = "project.native.report"; //event.data["exoprt_wizard"];

        parent_app._rpc({
            model: 'gantt.native.tool',
            method: 'exist_model',
            args: ['project_native_report_advance'],
            context: parent_app.state.contexts
            }).then(function(data) {
                self.export_open(parent_app, res_model, context)
            });
    },


    export_open: function(parent, res_model, context) {
        new dialogs.FormViewDialog(parent, {
            res_model: res_model,
            res_id: false,
            context: context,
            title: _t("PDF Report for Screen"),
        }).open();
    }




});



return {

    OptionsItem : GanttListOptionsItem

};


});