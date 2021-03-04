import logging
from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta, date


class Outplacement(models.Model):
    _inherit = "res_partner"
