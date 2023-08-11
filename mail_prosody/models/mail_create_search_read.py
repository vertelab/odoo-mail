import logging
from odoo import fields, models, api, _
import xml.etree.ElementTree as ET
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)


class MailMessage(models.Model):
    _inherit = "mail.message"

    prosody_message_id = fields.Char(string="Prosody Message ID")

    @api.model_create_multi
    def create(self, vals):
        res = super(MailMessage, self).create(vals)
        return res

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        keys = self.fields_get()
        for i, dom in enumerate(domain):
            field = dom[0]
            if 'many2one' in keys[field]["type"]:
                try:
                    possible_int = int(domain[i][2])
                except Exception as e:
                    pass
                else:
                    domain[i][2] = possible_int
            elif 'many2many' in keys[field]["type"]:
                try:
                    possible_int = int(domain[i][2])
                except:
                    pass
                else:
                    domain[i][2] = possible_int
        res = super().search_read(domain, fields, offset, limit, order)
        return res


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
        return super().create(vals_list)