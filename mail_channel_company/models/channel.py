from odoo import models, fields, api

class MailChannel(models.Model):
    _inherit = 'discuss.channel'

    auto_subscribe_company_id = fields.Many2one('res.company', string='Auto Subscription Company', help="Users of this company will auto-subscribe to this channel")

    @api.model
    def _auto_subscribe_users_to_channel(self, channel):
        if not channel.auto_subscribe_company_id:
            return
        company = channel.auto_subscribe_company_id
        users = self.env['res.users'].search([('company_ids', 'in', company.id)])
        partners = users.mapped('partner_id')
        # Add partners to channel subscribers if not already present
        to_subscribe = partners - channel.channel_partner_ids
        if to_subscribe:
            channel.channel_partner_ids |= to_subscribe

    @api.model
    def _auto_unsubscribe_users_from_channel(self, channel):
        if not channel.auto_subscribe_company_id:
            return
        company = channel.auto_subscribe_company_id
        users = self.env['res.users'].search([('company_ids', 'not in', company.id)])
        partners = users.mapped('partner_id')
        to_unsubscribe = channel.channel_partner_ids & partners
        if to_unsubscribe:
            channel.channel_partner_ids -= to_unsubscribe

    def update_auto_subscriptions(self):
        for channel in self.search([('auto_subscribe_company_id', '!=', False)]):
            self._auto_subscribe_users_to_channel(channel)
            self._auto_unsubscribe_users_from_channel(channel)

