
import logging
from odoo import api, fields, models, _

from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class GanttNativePredecessor(models.AbstractModel):
    _name = 'gantt.native.predecessor'
    _description = "gantt.native.predecessor"


    @api.model
    def _get_link_type(self):
        value = [
            ('FS', _('Finish to Start (FS)')),
            ('SS', _('Start to Start (SS)')),
            ('FF', _('Finish to Finish (FF)')),
            ('SF', _('Start to Finish (SF)')),

        ]
        return value

    type = fields.Selection('_get_link_type',
                            string='Type',
                            required=True,
                            default='FS')


    @api.model
    def _get_lag_type(self):
        value = [
            ('minute', _('minute')),
            ('hour', _('hour')),
            ('day', _('day')),
            ('percent', _('percent')),
        ]
        return value

    lag_type = fields.Selection('_get_lag_type',
                                string='Lag type',
                                required=True,
                                default='day')

    lag_qty = fields.Integer(string='Lag', default=0)

