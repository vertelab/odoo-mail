import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class MassMailing(models.Model):
    _inherit = "mail.mass_mailing"

    @api.model
    def search_count_extended(self, domain, domain_model):
        valid_models = [('model', '=', domain_model)] + self._fields['mailing_model_id'].domain
        if not self.env['ir.model'].search_count(valid_models):
            msg = f'Faulty model: {domain_model}'
            _logger.error(msg)
            raise UserError(msg)
        groups = self.env['ir.config_parameter'].get_param(
            'mass_mailing_allowed_search_groups', '')
        # Split and filter groups in to a list of groups with extra
        # spaces removed.
        groups = [x.strip() for x in groups.split(',') if x.strip()]
        # Make sure there are any groups and raise error if parameter is not set.
        if not groups:
            raise UserError(_('Config parameter mass_mailing_allowed_search_groups'
                              ' is not set contact your administrator'))
        if any([self.env.user.has_group(group) for group in groups]):
            domain = domain or []
            return self.env[domain_model].sudo().search_count(domain)
        raise UserError(_('You have to be member of the group(s) {groups}.').format(groups=groups))
