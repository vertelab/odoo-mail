from odoo import models, api, fields, _


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def action_send_email(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference(
                'mail_outplacement_report', 'email_template_login_employee')[1]
        except ValueError:
            template_id = False
        self.env['mail.template'].browse(template_id).with_context(nadim_type='email').send_mail(
            self.id, email_values={'notification': True}, force_send=True)
