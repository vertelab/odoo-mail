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

