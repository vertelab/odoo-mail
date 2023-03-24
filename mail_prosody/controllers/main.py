import logging
import json

from odoo import http
from odoo.http import Response, request
from odoo.addons.rest_api.controllers.main import check_permissions, rest_cors_value, successful_response, error_response


_logger = logging.getLogger(__name__)


class Prosody(http.Controller):
    @http.route('/api/chat/channel', methods=['GET'], type='http', auth='none', csrf=False, cors=rest_cors_value)
    @check_permissions
    def api_search_channel(self, **kwargs):
        cr, uid = request.cr, request.session.uid
        if kwargs:
            channel_id = request.env(cr, uid)['mail.channel'].sudo().search_partner_channels(kwargs)
            _logger.warning("searched channel %s", channel_id)
            dict_data = {'channel_id': channel_id}
            return successful_response(status=200, dict_data=dict_data)
        return error_response(400, 'Bad Request', 'Some parameters are missing')

    @http.route('/api/chat', methods=['POST'], type='http', auth='none', csrf=False, cors=rest_cors_value)
    @check_permissions
    def api_chat(self, **kwargs):
        cr, uid = request.cr, request.session.uid
        if kwargs:
            kwargs['channel_id'] = int(kwargs.get("channel_id"))
            kwargs['subtype_id'] = int(kwargs.get("subtype_id"))
            channel_message = request.env(cr, uid)['mail.channel'].sudo().message_channel_post_chat(kwargs)
            _logger.warning("channel_message result =  %s", channel_message)
            dict_data = {'channel_message': channel_message}
            return successful_response(status=200, dict_data=dict_data)
        return error_response(400, 'Bad Request', 'Some parameters are missing')

    @http.route('/api/messages', methods=['GET'], type='http', auth='none', csrf=False, cors=rest_cors_value)
    @check_permissions
    def search_read_messages(self, **kwargs):
        _logger.warning("Incoming messages data %s", kwargs)
        cr, uid = request.cr, request.session.uid
        if kwargs:
            comment_messages = request.env(cr, uid)['mail.message'].sudo().search_read([
                ("message_type", "=", kwargs.get("message_type"))])
            dict_data = [{
                'id': message.get('id'),
                'create_date': str(message.get('create_date')),
                'date': str(message.get('date')),
            } for message in comment_messages]

            _logger.warning("channel_messages result =  %s", dict_data)
            return successful_response(status=200, dict_data=dict_data)
        return error_response(400, 'Bad Request', 'Some parameters are missing')

    @http.route('/api/channels', methods=['GET'], type='http', auth='none', csrf=False, cors=rest_cors_value)
    @check_permissions
    def search_read_channels(self, **kwargs):
        _logger.warning("Incoming channels data %s", kwargs)
        cr, uid = request.cr, request.session.uid
        channels = request.env(cr, uid)['mail.channel'].sudo().search_read([])
        dict_data = [{
            'id': channel.get('id'),
            'create_date': str(channel.get('create_date')),
            'channel_message_ids': channel.get('channel_message_ids')
        } for channel in channels]
        _logger.warning("channel_messages result =  %s", dict_data)
        return successful_response(status=200, dict_data=dict_data)
