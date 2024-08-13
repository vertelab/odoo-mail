from odoo import models, fields, api, tools, _
import logging
import os
from odoo.http import request

_logger = logging.getLogger(__name__)

class MailThread(models.AbstractModel):
    
    _inherit = "mail.thread"

    def _get_creation_message(self):
        res = super(MailThread,self)._get_creation_message()
        #return _('%s created') % doc_name

        _logger.warning(f"{request.httprequest.headers=}")
        _logger.warning(f"{os.environ=}")
        _logger.warning(f"{[r for r in request.httprequest.headers if 'X-Real-Ip' in r]}")
        _logger.warning(f"{[r for r in request.httprequest.headers if 'User-Agent' in r]}")
        # ~ _logger.warning(f"{[r for r in request.httprequest.headers.items()]}")
        return _('%s \n%s') % (res,[r for r in request.httprequest.headers if 'X-Real-Ip' in r])


    def _creation_message(self):
        res = super(MailThread,self)._creation_message()
        #return _('%s created') % doc_name

        _logger.warning(f"{request.httprequest.headers=}")
        _logger.warning(f"{os.environ=}")
        _logger.warning(f"{[r for r in request.httprequest.headers if 'X-Real-Ip' in r]}")
        _logger.warning(f"{[r for r in request.httprequest.headers if 'User-Agent' in r]}")
        # ~ _logger.warning(f"{[r for r in request.httprequest.headers.items()]}")
        return _('%s \n%s') % (res,[r for r in request.httprequest.headers if 'X-Real-Ip' in r])
