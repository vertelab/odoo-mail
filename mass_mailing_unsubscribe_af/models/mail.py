from odoo import _, api, fields, models


class MailUnsubscription(models.Model):
    _inherit = "mail.unsubscription"

    mass_mailing_id = fields.Many2one(
        "mail.mass_mailing",
        "Mass mailing",
        required=False,
        help="Mass mailing from which he was unsubscribed.")

    customer_id = fields.Char(help="Customer reference ID.", compute='_compute_customer_id')
    def _compute_customer_id(self):
        self.customer_id = getattr(self.sudo().unsubscriber_id, 'customer_id', '')
