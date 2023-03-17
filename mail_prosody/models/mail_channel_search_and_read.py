from distutils.util import change_root
import logging
import requests
import odoorpc
import re

from ntpath import join
from xml.dom import ValidationErr
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class ChannelSearchRead(models.Model):
    _inherit = "mail.channel"

    channel_email = fields.Char(string="XMPP Channel Email")

    def search_read_custom(self, domain=None, fields=None, offset=0, limit=None, order=None):
        res = super().search_read(domain, fields, offset, limit, order)
        return res 

    @api.model
    def search_custom(self, *args, offset=0, limit=None, order=None, count=False):
        new_args =[]
        for arg in args:
            new_arg = []
            for a in arg:
                new_arg.append(int(a) if a.isdigit() else a)
            new_args.append(new_arg)
        _logger.error(f"{new_args=}")
        res = super(ChannelSearchRead, self).search(new_args, offset, limit, order, count)
        return res.ids if res else 0

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, *, body='', subject=None, message_type='notification', email_from=None, author_id=None,
                     parent_id=False, subtype_xmlid=None, subtype_id=False, partner_ids=None, channel_ids=None,
                     attachments=None, attachment_ids=None, add_sign=True, record_name=False, **kwargs):

        res = super().message_post(body=body, subject=subject, message_type=message_type, email_from=email_from,
                                   author_id=author_id, parent_id=parent_id, subtype_xmlid=subtype_xmlid,
                                   subtype_id=subtype_id, partner_ids=partner_ids, channel_ids=channel_ids,
                                   attachments=attachments, attachment_ids=attachment_ids, add_sign=add_sign,
                                   record_name=record_name, **kwargs)

        if res.id and not kwargs.get("prosody"):
            url = self.env['ir.config_parameter'].get_param('prosody_url', 'https://lvh.me:5281/rest')
            if res.channel_ids.mapped('channel_partner_ids'):
                recipient_id = res.channel_ids.mapped('channel_partner_ids') - res.author_id
                data = {'body': body, 'kind': 'message', 'id': 'ODOOODOO' + str(res.id)}
                try:
                    if self.public == 'groups':
                        data.update({'to': self.channel_email, 'type': 'groupchat'})
                    else:
                        data.update({'to': recipient_id[0].email if recipient_id else False, 'type': 'chat'})
                    headers = {'Content-type': 'application/json'}
                    js = requests.post(url, json=data, headers=headers, verify=False, auth=(
                        self.env.user.login, self.env.user.xmpp_password))
                except Exception as e:
                    raise ValidationError(_(e))
        return res

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

    def _create_channel(self, channel_name, partner_ids, public='private', channel_type='chat'):
        channel_id = self.env[self._name].create({
            'name': channel_name,
            'channel_partner_ids': [(4, partner_id.id) for partner_id in partner_ids if partner_id],
            'public': public,
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

        channel_name = vals.get('sender').split("@")[0]   # vertel@lvh.me ==> vertel
        channel_id = self.env[self._name].search([('name', '=', channel_name)])

        if "invited" in vals.get('text_body'):
            invitee_jid = vals.get('recipient').split("@")[0]   # possible invitee demo@lvh.me ==> demo
            moderator_jid = re.findall(r'/([a-z]+)', vals.get("text_body"))
        else:
            status = "declined"
            invitee_jid = re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', vals.get("text_body"))[0].split("@")[0]
            moderator_jid = re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', vals.get("recipient"))[0].split("@")[0]

        moderator_partner_id = self._add_moderator_to_channel(moderator_jid=moderator_jid, channel_id=channel_id)
        invitee_partner_id = self._update_channel_with_other_participant(
            invitee_jid=invitee_jid, channel_id=channel_id, status=status
        )

        if not channel_id:
            channel_id = self._create_channel(
                channel_name=channel_name,
                partner_ids=[moderator_partner_id, invitee_partner_id],
                public='groups',
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
        if channel_id and (participant_partner_id not in channel_id.mapped('channel_partner_ids')) and status == "invited":
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
        partner_id = self.env['res.users'].search([('login', '=', sender_jid)], limit=1).mapped('partner_id')

        channel_id = self.env[self._name].search([('name', '=', channel_name)])

        if channel_id and (partner_id not in channel_id.mapped('channel_partner_ids')):
            channel_id.write({
                'channel_partner_ids': [(4, partner_id.id)],
            })
        if not channel_id:
            channel_id = self._create_channel(
                channel_name=channel_name,
                partner_ids=[partner_id],
                public='groups',
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
    def message_post_test(self, *args):
        for arg in args:
            if channel := self.env["mail.channel"].browse(arg.get('id')):
                _logger.error(f"{channel=}")
                new_arg = {a: arg[a] for a in arg}
                new_arg["prosody"] = True
                message_post = channel.message_post(**new_arg).id
                return message_post
