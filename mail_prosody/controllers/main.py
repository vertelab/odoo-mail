from odoo import http

_logger = logging.getLogger(__name__)


class Prosody(http.Controller):
    @http.route('/api/auth/', methods=['POST'], type='json', auth='none', csrf=False)
    def api_auth_user(self, **kw):
        _logger.warning("Incoming data %s", kw)
