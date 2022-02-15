import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import safe_eval as eval

_logger = logging.getLogger(__name__)

# Overriding default valid models with those we want.
MASS_MAILING_BUSINESS_MODELS = ['res.partner', 'mail.mass_mailing.list']

class MassMailing(models.Model):
    _inherit = "mail.mass_mailing"
    internal_name = fields.Char(string='Internt namn')
    mailing_model_id = fields.Many2one('ir.model', string='Recipients Model', domain=[('model', 'in', MASS_MAILING_BUSINESS_MODELS)])

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s' % rec.internal_name))
        return res

    @api.multi
    def put_in_queue(self):
        for rec in self:
            if not rec.body_html:
                raise UserError("Du måste välja en mall")
        super(MassMailing, self).put_in_queue()

    @api.onchange('mailing_domain')
    def add_email_filter(self):
        """Added email filter for search domain."""
        domain_list = eval(self.mailing_domain)
        email_is_set = ['email', '!=', False]
        if email_is_set not in domain_list:
            domain_list.append(email_is_set)
            self.mailing_domain = repr(domain_list)
            _logger.debug(f"Updated mailing domain to: {self.mailing_domain}.")

    # Override to remove customer = True from res.partner.
    @api.onchange('mailing_model_id', 'contact_list_ids')
    def _onchange_model_and_list(self):
        mailing_domain = []
        if self.mailing_model_name:
            if self.mailing_model_name == 'mail.mass_mailing.list':
                if self.contact_list_ids:
                    mailing_domain.append(('list_ids', 'in', self.contact_list_ids.ids))
                else:
                    mailing_domain.append((0, '=', 1))
            elif self.mailing_model_name == 'res.partner':
                pass
                #mailing_domain.append(('customer', '=', True))
            elif 'opt_out' in self.env[self.mailing_model_name]._fields and not self.mailing_domain:
                mailing_domain.append(('opt_out', '=', False))
        else:
            mailing_domain.append((0, '=', 1))
        self.mailing_domain = repr(mailing_domain)
        self.body_html = "on_change_model_and_list"
