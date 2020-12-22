from odoo import models, fields
import logging
_logger = logging.getLogger(__name__)

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def action_send_eletter(self):
        print ("send mail")
        _logger.warn('Test skipped because there is no chart of account defined ...')
        # template_id = self.env.ref(hr.employee.email_template_assigned_coach).id
        #self.env['mail.template'].browse(id ="3").send_mail(self.id, force_send=True)
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        _logger.warn('ir_model_data: %s' % ir_model_data)
        try:
            template_id = ir_model_data.get_object_reference('mail_outplacement_report',   'email_template_assigned_coach')[1]
            _logger.warn('template_id: %s' % template_id)            
        except ValueError:
            template_id = False
            _logger.warn('template_id: %s' % template_id)
        template_browse =self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)
        _logger.warn('Invalid log level: %s' % template_browse)