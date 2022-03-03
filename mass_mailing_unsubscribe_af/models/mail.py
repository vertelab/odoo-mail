from odoo import _, api, fields, models
from lxml import etree
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

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        result = super(MailUnsubscription, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)
        # Disabling the import button for users who are not in import group
        if view_type == 'tree':
            doc = etree.XML(result['arch'])
            for node in doc.xpath("//tree"):
                # Set the import to false
                node.set('create', 'false')
            result['arch'] = etree.tostring(doc)
        return result


class MassMailing(models.Model):
    _inherit = "mail.mass_mailing"

    total_unsubscribers = fields.Integer(string="total unsubscribers.", compute='_compute_unsubscribe_id')
    unsubscription_ratio_percent = fields.Float(string="unsubscription ratio rate", compute='_compute_unsubscribe_id')

    def _compute_unsubscribe_id(self):
        for record in self:
            res_blacklist = self.env['mail.unsubscription'].sudo().search(
                [('mass_mailing_id', '=', record.id),
                 ("action", "=", 'blacklist_add')])

            res_unsubscritption = self.env['mail.unsubscription'].sudo().search(
                [('mass_mailing_id', '=', record.id),
                 ("action", "=", 'unsubscription')])

            record.total_unsubscribers = len(res_blacklist) + len(res_unsubscritption)

            if int(record.sent) != 0:
                record.unsubscription_ratio_percent = 100 * record.total_unsubscribers / int(record.sent)


class MassMailingContact(models.Model):
    _inherit = 'mail.mass_mailing.contact'

    opt_out_reason = fields.Char(
        string="Orsak",
        compute="_compute_opt_out_reason"
    )

    def _compute_opt_out_reason(self):
        for rec in self:
            if rec.opt_out:
                last_opt_out = self.env['mail.unsubscription'].search(
                    [
                        ('email', '=', rec.email),
                        ('mailing_list_ids', 'in', rec.list_ids._ids),
                        ('action', 'in', ['unsubscription', 'blacklist_add'])
                    ],
                    order="date desc",
                    limit=1
                )
                if not last_opt_out:
                    last_opt_out = self.env['mail.unsubscription'].search(
                        [
                            ('email', '=', rec.contact_id.email),
                            ('action', 'in', ['blacklist_add'])
                        ],
                        order="date desc",
                        limit=1
                    )
                rec.opt_out_reason = last_opt_out.reason_id.name


class MassMailingContactListRel(models.Model):
    _inherit = 'mail.mass_mailing.list_contact_rel'

    opt_out_reason = fields.Char(
        string="Orsak",
        compute="_compute_opt_out_reason"
    )

    def _compute_opt_out_reason(self):
        for rec in self:
            if rec.opt_out:
                last_opt_out = self.env['mail.unsubscription'].search(
                    [
                        ('email', '=', rec.contact_id.email),
                        ('mailing_list_ids', 'in', rec.list_id.id),
                        ('action', 'in', ['unsubscription'])
                    ],
                    order="date desc",
                    limit=1
                )
                if not last_opt_out:
                    last_opt_out = self.env['mail.unsubscription'].search(
                        [
                            ('email', '=', rec.contact_id.email),
                            ('action', 'in', ['blacklist_add'])
                        ],
                        order="date desc",
                        limit=1
                    )
                rec.opt_out_reason = last_opt_out.reason_id.name

