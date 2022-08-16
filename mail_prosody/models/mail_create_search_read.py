from distutils.util import change_root
import logging
import requests
import odoorpc

from ntpath import join
from xml.dom import ValidationErr
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class MailMessage(models.Model):
    _inherit = "mail.message"

    @api.model
    def create(self, vals):
        print("+++", vals)

        res = super(MailMessage, self).create(vals)

        # channel_id = vals.get("id")
        # if channel_id:
        #     _logger.warning(f"CHANNEL ID: {channel_id}")
        #     channel = self.env["mail.channel"].search_read([("id", "=", channel_id)])
        #     _logger.warning(f"CHANNEL: {channel}")
        #     if channel:
        #         channel_partners = channel[0].get("channel_partner_ids")
        #         _logger.warning(f"CHANNEL PARTNER IDS: {self.env.user.partner_id.name}")

        # headers = {
        #     'Content-Type': 'text/plain',
        # }
        # data = 'MESSAGE HERE'
        # test = requests.post('http://hoary.vertel.se:5280/msg/to@hoary.vertel.se', headers=headers, data=data, auth=('admin@hoary.vertel.se', 'admin'))

        # _logger.warning(f"RES: {res}")
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
