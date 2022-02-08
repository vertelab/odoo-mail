import logging

from odoo import models, fields, api, _

class MassMailing(models.Model):
    _inherit = "mail.mass_mailing"
    internal_name = fields.Char(string='Internt namn')


    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s' % rec.internal_name))
        return res
