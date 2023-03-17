from distutils.util import change_root
import logging
import requests
import odoorpc

from ntpath import join
from xml.dom import ValidationErr
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class TestSearchRead(models.Model):
    _inherit = "res.users"

    def search_read_custom(self, domain=None, fields=None, offset=0, limit=None, order=None):
        res = super().search_read(domain, fields, offset, limit, order)
        _logger.warning(f"{res=}")
        return res
