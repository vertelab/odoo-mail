# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2022- Vertel AB (<https://vertel.se>).
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

{
    'name': 'Project: Mail Include Latest Message',
    'version': '18.0.1.0.3',
    'summary': 'Mail Include Latest Message',
    'category': 'Project',
    'description': """
        Mail Include Latest Message
    """,
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-mail/mail_include_latest_message',
    'images': ['static/description/banner.png'], # 560x280 px.
    'license': 'AGPL-3',
    'contributor': 'Vertel AB,',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-mail',
    'depends': [
        'mail',
        'im_livechat'
    ],
    'data': {
    },
    'assets': {
        'web.assets_backend': [
            'mail_include_latest_message/static/src/js/message_model_patch.js',
        ],
    },
    'application': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
