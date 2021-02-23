import logging
from odoo import models, api, fields, _
from datetime import datetime, timedelta, date

_logger = logging.getLogger(__name__)

LOCAL_TZ = 'Europe/Stockholm'


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


class Outplacement(models.Model):
    _inherit = "outplacement"

    date = fields.Date(string="Meeting date", help="Date of meeting")
    time = fields.Float(string="Meeting time", help="t.ex. 15:30")
    performing_operation_adress = fields.Many2one(
        comodel_name='res.partner',
        name='Adress', string='Performing Adress')

    @api.multi
    def action_send_eletter(self):
        template_id = self.env.ref('mail_outplacement_report.email_template_assigned_coach').id
        template = self.env['mail.template'].browse(template_id)
        template.with_context(nadim_type='eletter').send_mail(
            self.id, email_values={'notification': True}, force_send=True)

    # FUTURE USE FOR EDITABLE EMAIL TEMPLATES VIA POP-UP WIZARD
    # @api.multi
    # def action_send_eletter(self):
    #     """
    #     This function opens a window to compose an email, with the assigned coach template message loaded by default
    #     """
    #
    #     self.ensure_one()
    #     ir_model_data = self.env['ir.model.data']
    #     try:
    #         """
    #         Find the email template that we've created in data/assigned_coach_data.xml
    #         get_object_reference first needs the module name where the template is build and then the name
    #         of the email template (the record id in XML).
    #         """
    #         template_id = ir_model_data.get_object_reference(
    #         'mail_outplacement_report', 'email_template_assigned_coach')[1]
    #     except ValueError:
    #         template_id = False
    #
    #     try:
    #         """
    #         Load the e-mail composer to show the e-mail template in
    #         """
    #         compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
    #     except ValueError:
    #         compose_form_id = False
    #     ctx = {
    #         # Model on which you load the e-mail dialog
    #         'default_model': 'outplacement',
    #         'default_res_id': self.ids[0],
    #         """
    #         Checks if we have a template and sets it if Odoo found our e-mail template
    #         """
    #         'default_use_template': bool(template_id),
    #         'default_template_id': template_id,
    #         'default_composition_mode': 'comment',
    #         'force_email': True
    #     }
    #
    #     """
    #      Will show the e-mail dialog to the user in the frontend
    #     """
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'mail.compose.message',
    #         'views': [(compose_form_id, 'form')],
    #         'view_id': compose_form_id,
    #         'target': 'new',
    #         'context': ctx,
    #     }
