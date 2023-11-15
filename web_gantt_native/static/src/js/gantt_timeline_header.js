odoo.define('web_gantt_native.TimeLineHeader', function (require) {
"use strict";


var core = require('web.core');
var Widget = require('web.Widget');
var GanttHeaderHint = require('web_gantt_native.HeaderHint');



var GanttTimeLineHeader = Widget.extend({
    template: "TimelineGantt.header",

    events: {
        'mouseover  .task-gantt-bottom-column'    :'HandleTipOver',
        'mouseout   .task-gantt-bottom-column'    :'HandleTipOut',
    },

    init: function(parent, timeScale, timeType, first_scale, second_scale) {
        this._super(parent);

        this.timeScale = timeScale;
        this.timeType = timeType;

        this.first_scale = first_scale;
        this.second_scale = second_scale;

        this.TODAY = moment();
    },


    HandleTipOver: function(ev) {
        var self = this;
        if (ev.target['data-id']){

            if (self.__parentedParent.header_hint_widget) {
                self.__parentedParent.header_hint_widget.do_show();
            }
            self.__parentedParent.header_hint_widget.show_hint(ev.target, ev.pageX, ev.pageY )
        }
    },


    HandleTipOut: function(ev) {
        var self = this;
        if (self.__parentedParent.header_hint_widget) {
            self.__parentedParent.header_hint_widget.do_hide();
        }
    },


    start: function(){

        var self = this;
        var el = self.$el;
        let renderer = self.__parentedParent

        var gutterOffset = self.__parentedParent.local_storage.getItem("gantt_offset") || self.__parentedParent.gutterOffset;

        var el_gantt_items = el.find('.timeline-gantt-items');

        el_gantt_items.css("width", gutterOffset);


        var el_scale_primary = el.find('.timeline-gantt-scale-primary');
        var el_scale_secondary = el.find('.timeline-gantt-scale-secondary');

        var tip_el = self.__parentedParent.$('.task-gantt-line-tips')
        var gantt_header_hint = new GanttHeaderHint(self.__parentedParent);
        gantt_header_hint.appendTo(tip_el);
        self.__parentedParent.header_hint_widget = gantt_header_hint;


        if (this.timeType === 'day_1hour' ||
            this.timeType === 'day_2hour' ||
            this.timeType === 'day_4hour' ||
            this.timeType === 'day_8hour' ) {

            _.each(this.first_scale, function(range_date , rdate){

                var dm =  moment(rdate).format("Do MMM dd - YY");
                var monthScale = self.timeScale*range_date.length;

                var div_cell = $('<span class="task-gantt-top-column"></span>');
                    div_cell.css({ width: monthScale + "px" });
                    div_cell.append($('<span class="task-gantt-scale-month-text">'+dm+'</span>'));

                    el_scale_primary.append(div_cell);


                _.each(range_date, function(hour){

                    var div_cell ='';

                    var hours_string =  moment(hour).format("HH:mm");

                    div_cell = $('<span class="task-gantt-bottom-column">'+hours_string+'</span>');
                    div_cell.css({ width: self.timeScale + "px" });

                    if (moment(hour).isoWeekday() === 6 || moment(hour).isoWeekday() === 7){
                        div_cell.addClass('task-gantt-weekend-column');
                    }

                    if (moment(hour).isSame(self.TODAY, 'day')){
                        div_cell.addClass('task-gantt-today-column');
                    }

                    el_scale_secondary.append(div_cell);

                });
            });
        }



        if (this.timeType == 'month_day')
        {
            _.each(this.second_scale, function(day){

                var div_cell ='';

                div_cell = $('<span class="task-gantt-bottom-column">'+moment(day).date()+'</span>');
                div_cell.css({ width: self.timeScale + "px" });

                if (moment(day).isoWeekday() === 6 || moment(day).isoWeekday() === 7){
                    div_cell.addClass('task-gantt-weekend-column');
                }

                if (moment(day).isSame(self.TODAY, 'day')){
                    div_cell.addClass('task-gantt-today-column');
                }

                var day_s = moment(day).format('Do MMM dd (YY)');
                div_cell.prop('data-id',day_s);

                return  el_scale_secondary.append(div_cell);

            });

            _.each(this.first_scale, function(month){


                     var monthScale = self.timeScale*month.days;

                     var div_cell = $('<span class="task-gantt-top-column"></span>');
                     div_cell.css({ width: monthScale + "px" });
                     div_cell.append($('<span class="task-gantt-scale-month-text">' + month.year + ' - ' + month.month + '</span>'));


                     return el_scale_primary.append(div_cell);

            });

        }


        if (this.timeType == 'month_week') {


            _.each(this.first_scale, function(range_date , rdate){

                var dm =  moment(rdate,"YYYY").format("YYYY");

                var monthScale = self.timeScale*range_date.length;

                var div_cell = $('<span class="task-gantt-top-column"></span>');
                    div_cell.css({ width: monthScale + "px" });
                    div_cell.append($('<span class="task-gantt-scale-month-text">'+dm+'</span>'));

                    el_scale_primary.append(div_cell);


                _.each(range_date, function(week_num){

                        var div_cell ='';

                        var week_string =  moment(week_num).format("W");

                        let marker = "iW"
                        if (renderer.week_type === "week"){
                            marker = "W"
                        }

                        div_cell = $('<span class="task-gantt-bottom-column">'+week_string+'</span>');
                        div_cell.css({ width: self.timeScale + "px" });

                        var week_s = moment(week_num).startOf(renderer.week_type).format('Do MMM dd (YY)');
                        var week_e = moment(week_num).endOf(renderer.week_type).format('Do MMM dd (YY)');


                        div_cell.prop('data-id',marker+": "+week_string+": "+week_s+" - "+week_e);

                        if (moment(week_num).isSame(self.TODAY, 'week')){
                            div_cell.addClass('task-gantt-today-column');
                        }

                        el_scale_secondary.append(div_cell);


                });

            });

        }


        if (this.timeType == 'quarter') {


            _.each(this.first_scale, function(range_date , rdate){


                var dm =  moment(rdate,"YYYY").format("YYYY");

                var monthScale = self.timeScale*range_date.length;



                var div_cell = $('<span class="task-gantt-top-column"></span>');
                    div_cell.css({ width: monthScale + "px" });
                    div_cell.append($('<span class="task-gantt-scale-month-text">'+dm+'</span>'));

                    el_scale_primary.append(div_cell);


                _.each(range_date, function(quarter){

                        var div_cell ='';

                       var week_string =  moment(quarter).format("Q");

                        div_cell = $('<span class="task-gantt-bottom-column">'+week_string+'</span>');
                        div_cell.css({ width: self.timeScale + "px" });

                        el_scale_secondary.append(div_cell);
                });

            });


        }



        if (this.timeType == 'year_month') {


            _.each(this.first_scale, function(range_date , rdate){


               var dm =  moment(rdate,"YYYY").format("YYYY");

                var monthScale = self.timeScale*range_date.length;



                var div_cell = $('<span class="task-gantt-top-column"></span>');
                    div_cell.css({ width: monthScale + "px" });
                    div_cell.append($('<span class="task-gantt-scale-month-text">'+dm+'</span>'));

                    el_scale_primary.append(div_cell);


                _.each(range_date, function(quarter){

                        var div_cell ='';

                       var week_string =  moment(quarter).format("MMM");

                        div_cell = $('<span class="task-gantt-bottom-column">'+week_string+'</span>');
                        div_cell.css({ width: self.timeScale + "px" });

                        el_scale_secondary.append(div_cell);
                });

            });

        }





    }



});

return GanttTimeLineHeader;

});