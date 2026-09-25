# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2025- Vertel AB (<https://vertel.se>).
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
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
# __manifest__.py
{
    'website': 'https://vertel.se/apps/odoo-mail/mail_channel_company',
    'name': 'Mail: Channel Auto Subscription by Company',
    'version': '18.0.1.0.0',
    'category': 'Discuss',
    'license': 'AGPL-3',
    'summary': 'Auto subscribe users to channels based on company.',
    'description': '''
Channel Auto Subscription by Company
====================================

    Auto subscribe users to channels based on company.

    Features:

        - UI Integration: Extends 1 view(s) in the Odoo interface.
        - Extends Odoo: Builds on discuss.channel.
    ''',
    'depends': ['mail'],
    'data': [
        'views/mail_channel_views.xml',
    ],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
