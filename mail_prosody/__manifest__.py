# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2021 Vertel AB (<https://vertel.se>).
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

{
    'name': 'Odoo Chat',
    'version': '14.0.0',
    'category': 'other',
    'license': 'AGPL-3',
    'summary': 'Makes it easy to chat with prosody',
    'description': """Makes it easy to chat with prosody""",
    'author': 'Vertel AB',
    'website': 'https://vertel.se',
    'depends': ['base', 'mail', 'mail_bot'],
    'data': [
        "data/ir_config_parameter.xml",
        "views/mail_channel_view.xml",
    ],
    "external_dependencies": {
        'python': ['odoorpc'],
    },
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
