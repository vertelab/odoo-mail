import logging
from odoo import fields, models, api, _
import xml.etree.ElementTree as ET

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


class MailMessageProsodyArchiveProcessor(models.TransientModel):
    _name = 'mail.message.prosody.archive.processor'
    _description = "Prosody Archive to Mail Message"

    prosody_host = fields.Char(string="Host")

    prosody_user = fields.Char(string="User")

    prosody_store = fields.Char(string="Store")

    prosody_key = fields.Char(string="Key")

    prosody_with = fields.Char(string="With")

    prosody_value = fields.Text(string="Value")

    @api.depends('prosody_value')
    def _get_message_values(self):
        for rec in self:
            if rec.prosody_value:
                tree = ET.ElementTree(ET.fromstring(rec.prosody_value))
                root = tree.getroot()
                rec.message_id = root.attrib.get('id')
                rec.message_body = tree.find("body").text
                rec.recipient_id = self.env["res.users"].search([
                    ("email", "=", self._cleanup_p2p_mail(root.attrib.get('to')))
                ]).id
                rec.sender_id = self.env["res.users"].search([
                    ("email", "=", self._cleanup_p2p_mail(root.attrib.get('from')))
                ]).id
            else:
                rec.message_id = False
                rec.message_body = False
                rec.recipient_id = False
                rec.sender_id = False

    message_id = fields.Char(string="Message Id", compute=_get_message_values)

    message_body = fields.Char(string="Body", compute=_get_message_values)

    recipient_id = fields.Many2one("res.users", compute=_get_message_values, string="Recipient")

    sender_id = fields.Many2one("res.users", string="Odoo User", compute=_get_message_values)

    @api.depends('sender_id', 'recipient_id')
    def _get_channel(self):
        for rec in self:
            vals = {
                "sender": rec.sender_id.email,
                "recipient": rec.recipient_id.email,
                "message_type": "chat",
            }
            rec.channel_id = self.env['mail.channel'].search_partner_channels(vals)

    channel_id = fields.Many2one("mail.channel", string="Channel", compute=_get_channel)

    def _cleanup_p2p_mail(self, email):
        return email.split('/')[0]

    @api.depends('message_id', 'channel_id')
    def _trigger_mail_message(self):
        for rec in self:
            if rec.channel_id:
                mail_message_id = self.env["mail.message"].search([
                    ("prosody_message_id", "=", rec.message_id)
                ], limit=1)
                if not mail_message_id:
                    self.env["mail.message"].create({
                        "date": fields.Datetime.now(),
                        "email_from": f"{rec.sender_id.name} <{rec.sender_id.email}>",
                        "model": "mail.channel",
                        "res_id": rec.channel_id.id,
                        "author_id": rec.sender_id.partner_id.id,
                        "message_type": "comment",
                        "subtype_id": 1,
                        "record_name": f"{rec.channel_id.name}",
                        "body": rec.message_body,
                        "prosody_message_id": rec.message_id
                    })
                rec.chat_is_synced = True
            else:
                rec.chat_is_synced = False

    @api.model_create_multi
    def create(self, vals_list):
        res = super(MailMessageProsodyArchiveProcessor, self).create(vals_list)
        return res

    chat_is_synced = fields.Boolean(string="Is Synced", compute=_trigger_mail_message)