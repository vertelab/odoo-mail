import logging
import json

from odoo import http
from odoo.http import Response

_logger = logging.getLogger(__name__)


class Prosody(http.Controller):
    @http.route('/api/auth/', methods=['POST'], type='json', auth='none', csrf=False)
    def api_auth_user(self, **kw):
        _logger.warning("Incoming data %s", kw)
        headers = {'Content-Type': 'application/json'}
        body = {'results': {'code': 200, 'message': 'OK'}}

        return Response(json.dumps(body), headers=headers)
