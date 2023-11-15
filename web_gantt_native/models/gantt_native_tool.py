
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class GanttNativeTool(models.AbstractModel):
    _name = "gantt.native.tool"
    _description = 'Gantt Native Tool'

    @api.model
    def open_model(self, name_model, name_field):
        field_data = self.sudo().env['ir.model.fields']._get(name_model, name_field)
        return field_data.relation

    @api.model
    def exist_model(self, name_model):
        status = self.sudo().env['ir.module.module'].search([('name', '=', name_model)])
        if not status or status.state != 'installed':
            raise UserError(_('Please install module first: Gantt Native PDF Advance (project_native_report_advance). It free parts for: web_gantt_native '))
        return status


