import logging
from odoo.exceptions import ValidationError

from odoo import models, api, fields, _

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def name_get(self):
        context = self.env.context
        _logger.warning("context: %s" % context)
        if self.env.context.get('show_address'):
            # _logger.debug(" performing_operation_adress: %s" % self.show_address)
            res = []
            for partner in self:
                res.append((partner.id, '%s %s ' % (partner.street, partner.city)))
                # _logger.debug(" performing_operation_adress: %s" % self.show_address)
            return res
        else:
            return super(ResPartner, self).name_get()
