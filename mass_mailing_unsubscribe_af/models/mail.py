from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)



class MailUnsubscription(models.Model):
    _inherit = "mail.unsubscription"

    mass_mailing_id = fields.Many2one(
        "mail.mass_mailing",
        "Mass mailing",
        required=False,
        help="Mass mailing from which he was unsubscribed.")
    mass_mailing_internal_name = fields.Char(related="mass_mailing_id.internal_name")
    customer_id = fields.Char(help="Customer reference ID.", compute='_compute_customer_id')

    def _compute_customer_id(self):
        for rec in self:
            rec.customer_id = getattr(rec.sudo().unsubscriber_id, 'customer_id', '')


class MassMailing(models.Model):
    _inherit = "mail.mass_mailing"

    total_unsubscribers = fields.Integer(string="total unsubscribers.", compute='_compute_unsubscribe_id')
    unsubscription_ratio_percent = fields.Integer(string="unsubscription ratio rate", compute='_compute_unsubscribe_id')

    def _compute_unsubscribe_id(self):
        for record in self:
            res_blacklist = self.env['mail.unsubscription'].sudo().search(
                [('mass_mailing_id', '=', record.id),
                 ("action", "=", 'blacklist_add')])

            res_unsubscritption = self.env['mail.unsubscription'].sudo().search(
                [('mass_mailing_id', '=', record.id),
                 ("action", "=", 'unsubscription')])

            record.total_unsubscribers = len(res_blacklist) + len(res_unsubscritption)

            if record.sent != 0:
                record.unsubscription_ratio_percent = 100 * record.total_unsubscribers / record.sent
                _logger.warning("Haze ratio rate %s " %record.unsubscription_ratio_percent)
