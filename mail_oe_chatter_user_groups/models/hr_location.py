from odoo import models


class HrLocation(models.Model):
    _name = "hr.location"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'hr.location']
