import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ConfirmWizard(models.TransientModel):
    _name = 'send.confirm.wizard'

    def count_recipients(self):
        ids = self.env.context.get('active_ids', [])

        recipient_amount = 0
        for id_ in ids:
            record = self.env['mail.mass_mailing'].browse(id_)
            recipient_amount += len(record.get_recipients())
        msg = _('This will send the mail message to all recipients ({}).'
                ' Do you want to continue?')
        return msg.format(recipient_amount)
    message = fields.Char(default=count_recipients, readonly=True)

    def send_confirm(self):
        ids = self.env.context.get('active_ids', [])
        for id_ in ids:
            record = self.env['mail.mass_mailing'].browse(id_)
            record.put_in_queue()
