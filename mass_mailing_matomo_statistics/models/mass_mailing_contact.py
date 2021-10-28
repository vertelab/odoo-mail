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
            
