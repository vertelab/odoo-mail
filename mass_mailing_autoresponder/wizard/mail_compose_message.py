# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MailComposer(models.TransientModel):

    _inherit = 'mail.compose.message'

    body = fields.Html(default='')
