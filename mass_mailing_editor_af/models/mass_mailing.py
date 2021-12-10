import logging

from odoo import models, fields, api, _

class MassMailing(models.Model):
    _inherit = "mail.mass_mailing"
    internal_name = fields.Char(string='Internal name')
