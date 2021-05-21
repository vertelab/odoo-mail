# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _

class EventEmailAudit(models.Model):

    _name = 'event.email.audit'

    _description = 'Autoreponder Email Audit'

    user_id = fields.Many2one("res.users", "Sent through")
    partner_id = fields.Many2one("res.partner")
    email = fields.Char(related="partner_id.email", string="Email", store=True)
    sent_time = fields.Datetime("Sent Time")
    response = fields.Text("Response")
    event_id = fields.Many2one("partner.event", "Event")
    event_line_id = fields.Many2one("partner.event.email.schedule", "Event Line")

