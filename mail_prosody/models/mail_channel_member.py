import logging
from odoo import fields, models, api, _


class ChannelMember(models.Model):
    _inherit = 'mail.channel.member'

    @api.model_create_multi
    def create(self, vals_list):
        """Similar access rule as the access rule of the mail channel.

        It can not be implemented in XML, because when the record will be created, the
        partner will be added in the channel and the security rule will always authorize
        the creation.
        """
        vals_list = list(filter(lambda x: x.get("partner_id"), vals_list))
        res = super(ChannelMember, self).create(vals_list)
        if res.channel_id:
            res.channel_id._affiliation_data_query()
        return res