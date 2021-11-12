from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError
from odoo import tools
import uuid
import re
import logging
_logger = logging.getLogger(__name__)

class MassMailingContact(models.Model):
    _inherit = 'mail.mass_mailing.contact'
    def opt_out_all(self, name):
        for mass_mail in self.subscription_list_ids:
            mass_mail.opt_out = True

class MassMailingContactListRel(models.Model):
    _inherit = 'mail.mass_mailing.list_contact_rel'
    @api.onchange('opt_out')
    def onchange_opt_out(self):
        for contact in self:
            identical_mails = self.env['mail.mass_mailing.list_contact_rel'].search(
                [
                    ('contact_id.email', '=', contact.contact_id.email),
                    ('list_id.id', '=', contact.list_id.id)
                ])
            for email in identical_mails:
                email.write({'opt_out': contact.opt_out})
            
