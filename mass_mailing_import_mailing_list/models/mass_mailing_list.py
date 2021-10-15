# Copyright 2018 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields
import logging
_logger = logging.getLogger(__name__)


class MassMailingList(models.Model):
    _inherit = 'mail.mass_mailing.list'

    adkd_mail_name = fields.Char(string='ADKd mail name')
