import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def search_count_extended(self, domain=None):
        groups = self.env['ir.config_parameter'].get_param(
            'mass_mailing_allowed_search_groups_res_partner', '')
        # Split and filter groups in to a list of groups with extra
        # spaces removed.
        groups = [x.strip() for x in groups.split(',') if x.strip()]
        # Make sure there are any groups and raise error if parameter is not set.
        if not groups:
            raise UserError(_('Config parameter mass_mailing_allowed_search_groups_res_partner'
                              ' is not set contact your administrator'))
        if any([self.env.user.has_group(group) for group in groups]):
            domain = domain or []
            return self.sudo().search_count(domain)
        raise UserError(_('You have to be member of the group(s) {groups}.'.format(groups=groups)))
