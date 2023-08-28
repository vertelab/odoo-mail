import logging
import odoo
import re
import xmpp
import uuid
import psycopg2
import json
from odoo import http, SUPERUSER_ID, Command
from psycopg2 import sql

from odoo import fields, models, api, _
from odoo.exceptions import AccessError, UserError

import asyncio
import logging
from slixmpp import ClientXMPP
from slixmpp.plugins import xep_0045

_logger = logging.getLogger(__name__)


class MailChannel(models.Model):
    _inherit = "mail.channel"

    channel_email = fields.Char(string="XMPP Channel Email")

    @api.depends("prosody_room_password")
    def _compute_has_password(self):
        for rec in self:
            if rec.prosody_room_password:
                rec.has_password = True
            else:
                rec.has_password = False

    has_password = fields.Boolean(string="Has Password", compute=_compute_has_password)
    prosody_room_password = fields.Char(string="Prosody Room Password")

    def add_members(self, partner_ids=None, guest_ids=None, invite_to_rtc_call=False, open_chat_window=False,
                    post_joined_message=True):
        if self.has_password:
            raise AccessError("This channel is private, kindly contact prosody administrator to add you to the channel")
        return super(MailChannel, self).add_members(
            partner_ids=partner_ids,
            guest_ids=guest_ids,
            invite_to_rtc_call=invite_to_rtc_call,
            open_chat_window=open_chat_window,
            post_joined_message=post_joined_message
        )

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, *, message_type='notification', **kwargs):
        res = super().message_post(message_type=message_type, **kwargs)

        if res.id and not kwargs.get("prosody"):
            self._update_prosodyarchive(res)
        return res

    def _update_prosodyarchive(self, res):
        channel_id = self.env[res.model].browse(int(res.res_id))

        if channel_id.channel_type in ['channel', 'group']:
            receiver = channel_id.channel_email
            chat_type = 'groupchat'
        else:
            recipient_id = channel_id.mapped('channel_partner_ids') - res.author_id
            recipient_id = self.env["res.users"].sudo().search([("partner_id", "=", recipient_id[0].id)], limit=1)
            receiver = recipient_id.email
            chat_type = 'chat'

        jabberid = self.env.user.email
        password = odoo.tools.config.get('admin_passwd', False)
        message = re.sub('<[^<]+?>', '', res.body)

        jid = xmpp.protocol.JID(jabberid)
        connection = xmpp.Client(server=jid.getDomain(), debug=True)
        connection.connect()
        connection.auth(user=jid.getNode(), password=password, resource=jid.getResource())
        d = connection.send(
            xmpp.protocol.Message(to=receiver, body=message, typ=chat_type, subject=f'odoo-{uuid.uuid4()}'))
        print(d)

    @api.model
    def search_partner_channels(self, *kwargs):
        kwargs_vals = kwargs[0]
        sender = kwargs_vals.get('sender')
        recipient = kwargs_vals.get('recipient')
        message_type = kwargs_vals.get('message_type')

        if message_type == 'chat':
            chat_channel = self._p2p_chat([sender, recipient])
        else:
            chat_channel = self._group_chat(kwargs_vals)

        return chat_channel.id

    def _p2p_chat(self, contacts):
        members = self._cleanup_p2p_contact(contacts)
        partner_ids = []
        for member in members:
            partner_ids.append(self.env['res.partner'].search([('email', '=', member)]).id)
        channel_ids = self.env[self._name].search([('channel_partner_ids', 'in', partner_ids)])

        partner_ids = self.env['res.partner'].browse(partner_ids)
        partner_names = ', '.join(partner.name for partner in partner_ids)
        sorted_partner_names = ', '.join(sorted(partner_names.split(', ')))

        chat_channel = channel_ids.filtered(
            lambda channel: ', '.join(sorted(channel.name.split(', '))) == sorted_partner_names
        )

        if not chat_channel:
            channel_name = ', '.join(partner_id.name for partner_id in partner_ids)
            chat_channel = self._create_channel(channel_name, partner_ids)
        return chat_channel

    def _create_channel(self, channel_name, partner_ids, channel_type='chat'):
        channel_id = self.env[self._name].create({
            'name': channel_name,
            'channel_partner_ids': [(4, partner_id.id) for partner_id in partner_ids if partner_id],
            'channel_type': channel_type
        })
        return channel_id

    def _group_chat(self, vals):
        if vals.get('message_type') == "invitation":
            channel_id = self._group_invitation_handler(vals)
        else:
            channel_id = self._group_message_handler(vals)
        return channel_id

    def _group_invitation_handler(self, vals):
        status = "invited"

        channel_name = vals.get('sender').split("@")[0]  # vertel@lvh.me ==> vertel
        # search channel mail first
        channel_id = self.env[self._name].search([('channel_email', '=', vals.get('sender'))], limit=1)
        if not channel_id:
            channel_id = self.env[self._name].search([('name', '=', channel_name)])

        if "invited" in vals.get('text_body'):
            invitee_jid = vals.get('recipient').split("@")[0]  # possible invitee demo@lvh.me ==> demo
            moderator_jid = re.findall(r'/([a-z]+)', vals.get("text_body"))
        else:
            status = "declined"
            invitee_jid = re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', vals.get("text_body"))[0].split("@")[0]
            moderator_jid = re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', vals.get("recipient"))[0].split("@")[
                0]

        moderator_partner_id = self._add_moderator_to_channel(moderator_jid=moderator_jid, channel_id=channel_id)
        invitee_partner_id = self._update_channel_with_other_participant(
            invitee_jid=invitee_jid, channel_id=channel_id, status=status
        )

        if not channel_id:
            channel_id = self._create_channel(
                channel_name=channel_name,
                partner_ids=[moderator_partner_id, invitee_partner_id],
                channel_type='channel'
            )
            channel_id.write({'channel_email': vals.get('sender')})
        return channel_id

    def _add_moderator_to_channel(self, moderator_jid, channel_id):
        moderator_partner_id = self.env['res.users'].search([
            ('login', '=', moderator_jid)], limit=1).mapped('partner_id')
        if channel_id and moderator_partner_id not in channel_id.mapped('channel_partner_ids'):
            channel_id.write({'channel_partner_ids': [(4, moderator_partner_id.id)]})
        return moderator_partner_id

    def _update_channel_with_other_participant(self, invitee_jid, channel_id, status="invited"):
        participant_partner_id = self.env['res.users'].search([
            ('login', '=', invitee_jid)], limit=1).mapped('partner_id')
        if channel_id and (
                participant_partner_id not in channel_id.mapped('channel_partner_ids')) and status == "invited":
            channel_id.write({'channel_partner_ids': [(4, participant_partner_id.id)]})
        if channel_id and (participant_partner_id in channel_id.mapped('channel_partner_ids')) and status == "declined":
            channel_id.write({'channel_partner_ids': [(3, participant_partner_id.id)]})
        return participant_partner_id

    def _group_message_handler(self, contact):
        if contact.get('recipient'):
            channel_name = contact.get('recipient').split('@')[0]
            channel_alias = contact.get('recipient')
        else:
            channel_alias = re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', contact.get('sender'))[0]
            channel_name = channel_alias.split("@")[0]
        sender_jid = re.findall(r'/([a-z]+)', contact.get('sender'))
        partner_id = self.env['res.users'].search([('login', '=', sender_jid[0])], limit=1).mapped('partner_id')

        # search channel mail first
        channel_id = self.env[self._name].search([('channel_email', '=', channel_alias)], limit=1)
        if not channel_id:
            channel_id = self.env[self._name].search([('name', '=', channel_name)])

        if channel_id and (partner_id not in channel_id.mapped('channel_partner_ids')):
            channel_id.write({
                'channel_partner_ids': [(4, partner_id.id)],
            })
        if not channel_id:
            channel_id = self._create_channel(
                channel_name=channel_name,
                partner_ids=[partner_id],
                channel_type='channel'
            )
        channel_id.write({'channel_email': channel_alias})
        return channel_id

    def _cleanup_p2p_contact(self, emails):
        cleaned_email = []
        for email in emails:
            cleaned_email.append(email.split('/')[0])
        return cleaned_email

    @api.model
    def message_channel_post_chat(self, *args):
        print(args)
        for arg in args:
            if channel := self.env["mail.channel"].browse(arg.get('channel_id')):
                new_arg = {a: arg[a] for a in arg}
                new_arg["prosody"] = True
                message_post = channel.message_post(**new_arg).id
                return message_post

    def search_read_custom(self, domain=None, fields=None, offset=0, limit=None, order=None):
        res = super().search_read(domain, fields, offset, limit, order)
        return res

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        if res and res.channel_email:
            jabberid = xmpp.protocol.JID(res.channel_email)
            password = odoo.tools.config.get('admin_passwd', False)
            jabberid = self.env.user.email
            nickname = self.env.user.email.split('@')[0]

            from . import prosody_muc
            from odoo.addons.queue_job.delay import group, chain

            loop = asyncio.get_event_loop()

            # loop = asyncio.get_event_loop()
            # loop.run_in_executor(None, self.create_and_configure_muc_room, jabberid, password)

            # loop = asyncio.get_event_loop()
            # loop.run_until_complete(self.create_and_configure_muc_room(jabberid, password=password))

        return res

    @api.model
    def create_and_configure_muc_room(self, jid, password):
        xmpp = ClientXMPP(jid, password)
        xmpp.register_plugin('xep_0045')  # Register the xep_0045 plugin

        async def start(event):
            await xmpp.get_roster()
            xmpp.send_presence()
            await create_room()

        async def create_room():
            room_name = "helloworld"
            room_domain = "conference.rita.vertel.se"
            room_jid = f"{room_name}@{room_domain}"

            await xmpp.plugin['xep_0045'].join_muc(room_jid, "admin")

            form = await xmpp.plugin['xep_0045'].get_room_config(room_jid)
            form['muc#roomconfig_roomname'] = 'Hello World Room'
            form['muc#roomconfig_publicroom'] = True

            await xmpp.plugin['xep_0045'].set_room_config(room_jid, form)

        xmpp.add_event_handler("session_start", start)

        loop = xmpp.loop
        loop.run_until_complete(xmpp.connect())
        loop.run_until_complete(xmpp.process())


    @api.model
    def create_prosody_channel(self, *kwargs):
        dict_data = {}
        kwargs = kwargs[0]

        if kwargs.get("jid"):
            channel_id = self.env['mail.channel'].sudo().search([("channel_email", "=", kwargs.get("jid"))])

            partner_ids = []
            for member in kwargs.get("occupants").split(","):
                partner_ids.append(self.env['res.users'].sudo().search([('login', '=', member)]).partner_id)

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
                self.env['mail.channel'].sudo().create(channel_vals)

            if channel_id:
                partner_ids = self.env['res.partner'].sudo().browse([
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

        print(dict_data)
        return dict_data
