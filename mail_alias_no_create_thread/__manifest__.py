# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) {year} {company} (<{mail}>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
#
# https://www.odoo.com/documentation/14.0/reference/module.html
#
{
    'name': 'Stop Mail Thread Messeges',
    'version': '14.0.0.0.0',
    'summary': """Stop Mail Thread Messeges""",
    'category': '',
    'description': """Makes it so that a mail alias connected to a modele have a option for if thay want to be able to have mail thread as messages on thos models""",
    #'sequence': 1,
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-',
    'images': ['static/description/banner.png'], 
    'license': 'AGPL-3',
    'depends': ['mail'],
    'data': ["views/mail_alias_view.xml"],
    'demo': [],
    'application': False,
    'installable': True,    
    'auto_install': False,
}
