from odoo import models, api, _, fields
import logging

_logger = logging.getLogger(__name__)

class HrEmployee(models.Model):
    _inherit = "outplacement"

    @api.multi
    def action_send_email(self):
        template_id = self.env.ref('mail_outplacement_report.email_template_login_employee').id
        _logger.warn("ALDIN: template_id1: %s" % template_id)
        template = self.env['mail.template'].browse(template_id)
        _logger.warn("ALDIN: template: %s" % template)
        _logger.warn("ALDIN: self: %s" % self)
        result = template.send_mail(self.id, force_send=True)
        _logger.warn("ALDIN: result: %s" % result)

