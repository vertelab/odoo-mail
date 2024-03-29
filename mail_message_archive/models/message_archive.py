# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA,  Open Source Management Solution, third party addon
#    Copyright (C) 2021 Vertel AB (<https://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation,  either version 3 of the
#    License,  or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not,  see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api, _
from datetime import timedelta
#from random import choice
#from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import Warning

import time
import datetime
import dateutil
import pytz

import logging
_logger = logging.getLogger(__name__)


class MessageArchive(models.Model):
    _inherit = 'mail.message'
    _description = 'Mail Message'

    active = fields.Boolean(string='Active')
    
    
