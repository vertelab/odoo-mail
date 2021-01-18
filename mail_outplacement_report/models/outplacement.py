from odoo import models, api, _, fields
import logging

_logger = logging.getLogger(__name__)

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def action_send_email(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        _logger.warn("DAER: ir_model_data: %s" % ir_model_data)
        try:
            
            template_id = ir_model_data.get_object_reference('mail_outplacement_report', 'email_template_login_employee')[1]
            _logger.warn("DAER: template_id1: %s" % template_id)
        except ValueError:
            template_id = False
            _logger.warn("DAER: template_id: %s" % template_id)
        template_browse =self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)
        _logger.warn("DAER: template_browse: %s" % template_browse)

class Outplacement(models.Model):
    _inherit = "outplacement"

    @api.multi
    def action_send_eletter(self):
        template_id = self.env.ref('mail_outplacement_report.email_template_assigned_coach').id
        _logger.warn("ALDIN: template_id1: %s" % template_id)
        template = self.env['mail.template'].browse(template_id)
        _logger.warn("ALDIN: template: %s" % template)
        _logger.warn("ALDIN: self: %s" % self)
        result = template.send_mail(self.id, force_send=True)
        _logger.warn("ALDIN: result: %s" % result)

