# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2021 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, models, fields
import logging
_logger = logging.getLogger(__name__)


class MassMailingList(models.Model):
    _inherit = 'mail.mass_mailing.list'

    adkd_mail_name = fields.Char(string='ADKd mail name')
    is_adkd_campaign = fields.Boolean(string='ADKd Campaign') # Will not be needed
    list_type = fields.Char(string='List type')
    parent_id = fields.Many2one(comodel_name='mail.mass_mailing.list')
