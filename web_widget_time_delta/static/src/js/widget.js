odoo.define('web_widget_time_delta.TimeDelta', function(require) {
    "use strict";

    var field_registry = require('web.field_registry');
    var fields = require('web.basic_fields');

    var core = require('web.core');
    var _t = core._t;

    var FieldTimeDelta = fields.FieldChar.extend({

        template: 'FieldTimeDelta',
        widget_class: 'oe_form_field_time_delta',

        init: function () {

            this._super.apply(this, arguments);
            this.mask_humanize = undefined;
            this.showDays = false;
            this.showSeconds = false;

            if ("mask_humanize_string" in this.nodeOptions) {
                this.mask_humanize = this.nodeOptions["mask_humanize_string"];
            }

            if ("mask_humanize_field" in this.nodeOptions) {
                this.mask_humanize = this.recordData[this.nodeOptions["mask_humanize_field"]];
            }

            var mask_picker = "";
            if ("mask_picker_string" in this.nodeOptions) {
                mask_picker = this.nodeOptions["mask_picker_string"];

                if (mask_picker === "day_second"){
                    this.showDays = true;
                    this.showSeconds = true;
                }
                if (mask_picker === "day"){
                    this.showDays = true;
                }
                if (mask_picker === "second"){
                    this.showSeconds = true;
                }
            }

            if ("mask_picker_field" in this.nodeOptions) {
                mask_picker = this.recordData[this.nodeOptions["mask_picker_field"]];

                if (mask_picker === "day_second"){
                    this.showDays = true;
                    this.showSeconds = true;
                }
                if (mask_picker === "day"){
                    this.showDays = true;
                }
                if (mask_picker === "second"){
                    this.showSeconds = true;
                }
            }

        },

        _renderReadonlyValue: function (value) {

            if (this.mask_humanize){
                return  humanizeDuration(value*1000,{ units: this.mask_humanize.split(","),  round: true});
            }
            else{
                return humanizeDuration(value*1000);
            }
        },

        _renderReadonly: function () {
            var total = parseInt(this.value, 10);
            this.$el.text(this._renderReadonlyValue(total));
        },

        _getValue: function () {
            var $input = this.$el.find('input');
            return $input.val();
        },

        _renderEdit: function () {

            var show_value = parseInt(this.value, 10);

            if (this.hasOwnProperty('$input') && this.$input.data('durationPicker')) {
                var is_duration = this.$input.data('durationPicker')
                is_duration.setValue(show_value)
            }
            else{

                var $input = this.$el.find('input');
                $input.val(show_value);
                var self = this;
                $input.durationPicker({
                  translations: {
                        day: _t('day'),
                        hour:  _t('hour'),
                        minute:  _t('minute'),
                        second:  _t('second'),
                        days:  _t('days'),
                        hours:  _t('hours'),
                        minutes:  _t('minutes'),
                        seconds:  _t('seconds')
                      },

                    showSeconds: self.showSeconds,
                    showDays:  self.showDays,
                    onChanged: function (newVal) {
                        $input.val(newVal);
                    }
                });
                this.$input = $input;

            }
        },

    });

    field_registry
        .add('time_delta_list', FieldTimeDelta)
        .add('time_delta', FieldTimeDelta);

return {
    FieldTimeDelta: FieldTimeDelta
};

});
