

odoo.define('web_gantt_native.InterSection', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var time = require('web.time');



    var GanttTimeLineInterSection = Widget.extend({
        template: "GanttTimeLine.intersection",

        init: function(parent) {
            this._super.apply(this, arguments);

        },


        get_position_x: function(gantt_date_start, gantt_date_stop, parent){

            var task_start_time = gantt_date_start.getTime();
            var task_stop_time = gantt_date_stop.getTime();

            var task_start_pxscale = Math.round((task_start_time-parent.firstDayScale) / parent.pxScaleUTC);
            var task_stop_pxscale = Math.round((task_stop_time-parent.firstDayScale) / parent.pxScaleUTC);

            var bar_left = task_start_pxscale;
            var bar_width = task_stop_pxscale-task_start_pxscale;

            return {
                bar_left: bar_left,
                bar_width: bar_width,
            };

        },

        start: function(){
            // var self = this;

            let parentg =  this.getParent();

            if (parentg.industry_show) {

                let  get_position_x= this.get_position_x

                let $zTree = parentg.widget_ztree.$zTree;
                // let nodes = $zTree.getNodes();

                let data_widgets =  parentg.gantt_timeline_data_widget;


                _.each(data_widgets, function(widget) {
                    if (widget.record.is_group) {
                        let el = widget.$el
                        let node =  $zTree.getNodeByParam("zt_id", widget.record.zt_id, null);

                        let before_left = false
                        let before_top = 0

                        let childNodes = $zTree.transformToArray(node);

                        let sorted_childNodes = _.sortBy(childNodes, 'task_start');

                        _.each(sorted_childNodes, function (child) {

                            if (child["id"] !== undefined) {

                                let id = child["id"]
                                //Gantt Bar
                                var gantt_bar = $('<div class="task-gantt-bar-intersection"></div>');
                                gantt_bar.prop('id', "task-gantt-bar-intersection-" + id);

                                //Possition X
                                var get_possition = get_position_x(child.task_start, child.task_stop, parentg);

                                var bar_name = $('<div class="task-gantt-name">'+ child.value_name +'</div>');
                                bar_name.css({"width": get_possition.bar_width-5 + "px"});
                                gantt_bar.append(bar_name);


                                if (before_left && before_left > get_possition.bar_left){

                                    if (before_top === 0){
                                        before_top = 16
                                    }
                                    else{
                                        before_top = 0
                                    }
                                }

                                before_left = get_possition.bar_left +  get_possition.bar_width

                                gantt_bar.css({"top": before_top + "px"});
                                gantt_bar.css({"left": get_possition.bar_left + "px"});
                                gantt_bar.css({"width": get_possition.bar_width + "px"});

                                gantt_bar.css({"background": "rgba(242, 133, 113, 0.6)"});

                                el.append(gantt_bar);

                            }
                        })
                    }
                })
            }
        }
    });

    return {
        InterSectionWidget: GanttTimeLineInterSection
    }

});









