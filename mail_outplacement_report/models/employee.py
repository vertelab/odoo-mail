from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = "outplacement"

    def action_send_eletter(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('mail_outplacement_report', 'email_template_assigned_coach')[1]
        except ValueError:
            template_id = False
        template_browse =self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)
