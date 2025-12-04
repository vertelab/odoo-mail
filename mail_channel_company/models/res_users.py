from odoo import models, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        user = super().create(vals)
        user._update_user_channels()
        return user

    def write(self, vals):
        res = super().write(vals)
        self._update_user_channels()
        return res

    def _update_user_channels(self):
        channels = self.env['discuss.channel'].search([('auto_subscribe_company_id', 'in', self.company_ids.ids)])
        for channel in channels:
            if self.partner_id not in channel.channel_partner_ids:
                channel.channel_partner_ids |= self.partner_id
        # Also remove user from channels where company no longer matches
        remove_channels = self.env['discuss.channel'].search([
            ('auto_subscribe_company_id', '!=', False),
            ('id', 'not in', channels.ids)
        ])
        for channel in remove_channels:
            if self.partner_id in channel.channel_partner_ids:
                channel.channel_partner_ids -= self.partner_id


