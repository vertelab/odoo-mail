from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class Outplacement(models.Model):
    _inherit = "outplacement"

    performing_date = fields.Date(string="Meeting date", help="Date of meeting")
    performing_time = fields.Float(string="Meeting time", digits=(12, 2), copy=False, help="t.ex. 15:30")
    performing_operation_adress = fields.Many2one(
        comodel_name='res.partner',
        name='Adress', string='Performing Adress')

    @api.depends('performing_operation_adress')
    def _compute_per_op_address(self):
        if self.performing_operation_adress:
            self.per_op_address_text = self.performing_operation_adress.street + ',' + ' ' + \
                                       self.performing_operation_adress.zip + ' ' + \
                                       self.performing_operation_adress.city
        else:
            self.per_op_address_text = False

    per_op_address_text = fields.Char(compute='_compute_per_op_address', string='Performing address')

    @api.multi
    def action_send_eletter(self):
        if not self.performing_operation_id:
            raise ValidationError(_("Please enter Performing Operation field before sending email"))
        if not self.performing_operation_adress:
            raise ValidationError(_("Please enter meeting address before sending email"))
        if not self.performing_date:
            raise ValidationError(_("Please enter meeting date before sending email"))
        elif self.performing_time == 0:
            raise ValidationError(_("Please enter performing time before sending email"))
        else:
            template_id = self.env.ref('mail_outplacement_report.email_template_assigned_coach')
            template_id.with_context(nadim_type='eletter').send_mail(
                self.id, email_values={'notification': True}, force_send=True)

    #FOR FUTURE USE
    # @api.multi
    # def action_send_eletter(self):
    #     """
    #     This function opens a window to compose an email, with the assigned coach template message loaded by default
    #     """
    #     if not self.performing_operation_id:
    #         raise ValidationError(_("Please enter Performing Operation field before sending email"))
    #     if not self.performing_operation_adress:
    #         raise ValidationError(_("Please enter Performing address field before sending email"))
    #     if not self.performing_date:
    #         raise ValidationError(_("Please enter Meeting date field before sending email"))
    #     elif self.performing_time == 0:
    #         raise ValidationError(_("Please enter Meeting time before sending email"))
    #     else:
    #         self.ensure_one()
    #         ir_model_data = self.env['ir.model.data']
    #         try:
    #             template_id = ir_model_data.get_object_reference(
    #                 'mail_outplacement_report', 'email_template_assigned_coach')[1]
    #         except ValueError:
    #             template_id = False
    #
    #         try:
    #             compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
    #         except ValueError:
    #             compose_form_id = False
    #         ctx = {
    #             # Model on which you load the e-mail dialog
    #             'default_model': 'outplacement',
    #             'default_res_id': self.ids[0],
    #             'default_use_template': bool(template_id),
    #             'default_template_id': template_id,
    #             'default_composition_mode': 'comment',
    #             'force_email': True
    #         }
    #
    #         return {
    #             'type': 'ir.actions.act_window',
    #             'view_type': 'form',
    #             'view_mode': 'form',
    #             'res_model': 'mail.compose.message',
    #             'views': [(compose_form_id, 'form')],
    #             'view_id': compose_form_id,
    #             'target': 'new',
    #             'context': ctx,
    #         }
