import logging
import json

from odoo import http
from odoo.http import Response, request
from odoo.addons.rest_api.controllers.main import check_permissions, rest_cors_value, successful_response


_logger = logging.getLogger(__name__)


class Prosody(http.Controller):
    @http.route('/api/chat/channel', methods=['GET'], type='http', auth='none', csrf=False, cors=rest_cors_value)
    @check_permissions
    def api_search_channel(self, **kwargs):
        _logger.warning("Incoming data %s", kwargs)
        cr, uid = request.cr, request.session.uid
        if kwargs:
            channel_id = request.env(cr, uid)['mail.channel'].sudo().search_partner_channels(kwargs)
            _logger.warning("searched channel %s", channel_id)
            your_custom_dict_data = {'your_vals': '...'}
            return successful_response(status=200, dict_data=your_custom_dict_data)
        return successful_response(status=400, dict_data={})
