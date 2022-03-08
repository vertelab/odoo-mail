import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ConfirmWizard(models.TransientModel):
    _name = 'send.confirm.wizard'

    def count_recipients(self):
        """Count the amount of recipients and sanity check of records."""
        ids = self.env.context.get('active_ids', [])

        recipient_amount = 0
        for record in self.env['mail.mass_mailing'].browse(ids):
            self.check_validity(record)
            recipient_amount += len(record.sudo().get_recipients())
        msg = _('This will send the mail message to all recipients ({}).'
                ' Do you want to continue?')
        return msg.format(recipient_amount)
    message = fields.Char(default=count_recipients, readonly=True)

    @api.model
    def check_validity(self, record):
        """Sanity check of record."""
        if record.mailing_model_name == "mail.mass_mailing.list" and not record.contact_list_ids:
            raise UserError(_('You must select at least one recipient list.'))
        if not record.body_html:
            raise UserError(_("You have to select a template."))

    def send_confirm(self):
        """Runs on OK from user."""
        ids = self.env.context.get('active_ids', [])
        for record in self.env['mail.mass_mailing'].browse(ids):
            record.put_in_queue()
