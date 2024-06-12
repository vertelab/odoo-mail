from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class MailAlias(models.Model):
    
    _inherit = "mail.alias"

    no_message_on_replay = fields.Boolean(default=False)