from odoo import _, api, fields, models


class MailUnsubscription(models.Model):
    _inherit = "mail.unsubscription"

    mass_mailing_id = fields.Many2one(
        "mail.mass_mailing",
        "Mass mailing",
        required=False,
        help="Mass mailing from which he was unsubscribed.")
