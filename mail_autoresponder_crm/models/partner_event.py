from odoo import models, fields, api, _
import datetime
from odoo.tools.safe_eval import safe_eval


class PartnerEvent(models.Model):
    _inherit = 'partner.event'

    @api.model
    def _get_daily_partner(self):
        daily_notes = self.env['res.partner.notes'].search([('note_type.name', '=', '90'),
                                                            ('partner_id.segment_jobseeker', '=', 'a')])
        return [("notes_ids", "in", daily_notes.ids)]

    contact_domain = fields.Char(string="Search Filter", default=_get_daily_partner)
    customer_since = fields.Datetime(string="Customer since", related='user_id.partner_id.customer_since')
    deactualization_date = fields.Datetime(string="Deactualization", related='user_id.partner_id.deactualization_date')
    next_contact = fields.Date(string="Next Contact", related='user_id.partner_id.next_contact')
    last_contact = fields.Date(string="Last Contact", related='user_id.partner_id.last_contact')
