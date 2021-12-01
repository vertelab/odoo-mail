import logging

from odoo import models, fields, api, _
from odoo.tools import safe_eval as eval

_logger = logging.getLogger(__name__)


class MassMailing(models.Model):
    _inherit = "mail.mass_mailing"

    @api.onchange('mailing_domain')
    def add_email_filter(self):
        """Added email filter for search domain."""
        domain_list = eval(self.mailing_domain)
        email_is_set = ['email', '!=', False]
        if email_is_set not in domain_list:
            domain_list.append(email_is_set)
            self.mailing_domain = repr(domain_list)
            _logger.debug(f"Updated mailing domain to: {self.mailing_domain}.")