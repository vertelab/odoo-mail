import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError
class MassMailing(models.Model):
    _inherit = "mail.mass_mailing"
    internal_name = fields.Char(string='Internt namn')


    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s' % rec.internal_name))
        return res


    @api.multi
    def put_in_queue(self):
        for rec in self:
            if not rec.body_html:
                raise UserError("Du måste välja en mall")
        super(MassMailing, self).put_in_queue()
