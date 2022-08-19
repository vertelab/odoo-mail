from odoo import models, api, fields


class Users(models.Model):
    _inherit = 'res.users'

    xmpp_password = fields.Char(string="XMPP Password")

    @api.model
    def update_user_rec(self, *kwargs):
        vals = kwargs[0]
        user_id = self.env['res.users'].search([('login', '=', vals.get('login'))])
        if user_id:
            user_id.write({'xmpp_password': vals.get('password')})
            return True
        else:
            return False
