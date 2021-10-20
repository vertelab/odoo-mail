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


class MailMassMailing(models.Model):
    _inherit = "mail.mass_mailing"

    def update_opt_out(self, email, list_ids, value):
        """Save unsubscription reason when opting out from mailing."""
        # Check if list has ADKd parent then use that list instead.
        mail_list = self.env['mail.mass_mailing.list']
        if len(list_ids) == 1:
            mail_list = mail_list.search([('id', '=', list_ids[0])])
        if mail_list and mail_list.parent_id and mail_list.parent_id.is_adkd_campaign:
            list_ids[0] = mail_list.parent_id.id
        return super().update_opt_out(email, list_ids, value)
