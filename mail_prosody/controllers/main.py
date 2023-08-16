import logging
import json
from odoo import fields
from odoo import http, SUPERUSER_ID, Command
from odoo.http import Response, request
from odoo.addons.rest_api.controllers.main import check_permissions, successful_response, error_response

_logger = logging.getLogger(__name__)


class Prosody(http.Controller):
    def _cleanup_p2p_mail(self, email):
        return email.split('/')[0]

    @http.route('/api/prosodyarchive', methods=['GET'], type='http', auth='none', csrf=False)
    @check_permissions
    def api_prosody_archive(self, **kwargs):
        cr, uid = request.cr, request.session.uid
        if kwargs.get('sender'):
            channel_vals = {
                "sender": kwargs.get('sender'),
                "recipient": kwargs.get('recipient'),
                "message_type": kwargs.get('message_type'),
            }
            channel_id = request.env(cr, uid)['mail.channel'].sudo().search_partner_channels(channel_vals)

            chat_vals = {
                "body": kwargs.get('message_body'),
                "channel_id": channel_id.id,
                "subtype_id": 1,
                "message_type": 'comment',
                "prosody_message_id": kwargs.get('message_id'),
            }
            mail_message_id = request.env(cr, uid)["mail.message"].sudo().search([
                ("prosody_message_id", "=", kwargs.get('message_id'))
            ], limit=1)
            if not mail_message_id and chat_vals.get("body"):
                request.env(cr, uid)["mail.channel"].sudo().message_channel_post_chat(chat_vals)

    @http.route('/api/chat/channel', methods=['GET'], type='http', auth='none', csrf=False)
    @check_permissions
    def api_search_channel(self, **kwargs):
        cr, uid = request.cr, request.session.uid
        if kwargs:
            if kwargs.get("chat"):
                if kwargs.get("recipient") and kwargs.get("sender"):
                    channel_id = request.env(cr, uid)['mail.channel'].sudo().search_partner_channels(kwargs)
                    dict_data = {'channel_id': channel_id}
                    return successful_response(status=200, dict_data=dict_data)
                else:
                    return error_response(400, 'Bad Request', 'Some parameters are missing')

            channel_id = request.env(cr, uid)['mail.channel'].sudo().search_partner_channels(kwargs)
            dict_data = {'channel_id': channel_id}
            return successful_response(status=200, dict_data=dict_data)
        return error_response(400, 'Bad Request', 'Some parameters are missing')

    @http.route('/api/chat', methods=['POST', 'GET'], type='http', auth='none', csrf=False)
    @check_permissions
    def api_chat(self, **kwargs):
        cr, uid = request.cr, request.session.uid
        if kwargs:
            kwargs['channel_id'] = int(kwargs.get("channel_id"))
            kwargs['subtype_id'] = int(kwargs.get("subtype_id"))
            channel_message = request.env(cr, uid)['mail.channel'].sudo().message_channel_post_chat(kwargs)
            dict_data = {'channel_message': channel_message}
            return successful_response(status=200, dict_data=dict_data)
        return error_response(400, 'Bad Request', 'Some parameters are missing')

    @http.route('/api/messages', methods=['GET'], type='http', auth='none', csrf=False)
    @check_permissions
    def search_read_messages(self, **kwargs):
        cr, uid = request.cr, request.session.uid
        if kwargs:
            comment_messages = request.env(cr, uid)['mail.message'].sudo().search_read([
                ("message_type", "=", kwargs.get("message_type"))])
            dict_data = [{
                'id': message.get('id'),
                'create_date': str(message.get('create_date')),
                'date': str(message.get('date')),
            } for message in comment_messages]
            return successful_response(status=200, dict_data=dict_data)
        return error_response(400, 'Bad Request', 'Some parameters are missing')

    @http.route('/api/channels', methods=['GET'], type='http', auth='none', csrf=False)
    # @check_permissions
    def search_read_channels(self, **kwargs):
        cr, uid = request.cr, request.session.uid
        channels = request.env(cr, uid)['mail.channel'].sudo().search_read([])
        dict_data = [{
            'id': channel.get('id'),
            'create_date': str(channel.get('create_date')),
            'channel_message_ids': channel.get('channel_message_ids')
        } for channel in channels]
        return successful_response(status=200, dict_data=dict_data)

    @http.route('/channel', methods=['GET'], type='http', auth='none', csrf=False)
    # @check_permissions
    def create_channel(self, **kwargs):
        dict_data = {}
        cr, uid = request.cr, request.session.uid
        if kwargs.get("jid"):
            channel_id = request.env(cr, uid)['mail.channel'].sudo().search([("channel_email", "=", kwargs.get("jid"))])

            partner_ids = []
            for member in kwargs.get("occupants").split(","):
                partner_ids.append(request.env['res.users'].sudo().search([('login', '=', member)]).partner_id)

            channel_vals = {
                "prosody_room_password": kwargs.get("password", False),
                "description": kwargs.get("description", False),
            }

            if not channel_id:
                channel_vals.update({
                    'name': kwargs.get("jid").split("@")[0],
                    'channel_type': "channel",
                    'channel_email': kwargs.get("jid"),
                    'channel_member_ids': [
                        Command.create({
                            "partner_id": partner_id.id
                        })
                        for partner_id in partner_ids if partner_id
                    ]
                })
                request.env(cr, uid)['mail.channel'].sudo().create(channel_vals)

            if channel_id:
                partner_ids = request.env['res.partner'].sudo().browse([
                    partner_id.id for partner_id in partner_ids if partner_id
                ])

                absent_partner = partner_ids - channel_id.channel_member_ids.mapped('partner_id')

                channel_vals.update({
                    'channel_member_ids': [
                        Command.create({
                            "partner_id": partner_id.id
                        })
                        for partner_id in absent_partner if partner_id
                    ]
                })

                channel_id.sudo().write(channel_vals)
            dict_data.update({'channel_id': channel_id.id})
        return successful_response(status=200, dict_data=dict_data)

    @http.route('/muc/config', methods=['GET'], type='http', auth='none', csrf=False)
    # @check_permissions
    def muc_configuration(self, **kwargs):
        print(kwargs)
        config = {
            "affiliations": [
                {
                    "affiliation": "owner",
                    "jid": "admin@rita.vertel.se",
                    "nick": "admin"
                },
                {
                    "affiliation": "admin",
                    "jid": "demo@rita.vertel.se",
                    "nick": "demo"
                },
            ],
            "config": {
                "description": "Digital Discussions",
                "members_only": False,
                "moderated": False,
                "name": "The Digital",
                "persistent": True,
                "public": True,
                "subject": "Discussions regarding The Place"
            }
        }
        return config
