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
            new_arg=[]
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
            url = "https://lvh.me:5281/rest"
            if res.channel_ids.mapped('channel_partner_ids'):

                recipient_id = res.channel_ids.mapped('channel_partner_ids') - res.author_id
                data = {
                    'body': body,
                    'kind': 'message',
                    # 'from': res.author_id.email,
                    'id': 'ODOOODOO' + str(res.id),
                }
                if self.public == 'groups':
                    data.update({
                        'to': self.channel_email,
                        'type': 'groupchat',
                        'from': 'admin@lvh.me'
                    })
                else:
                    data.update({
                        'to': recipient_id[0].email if recipient_id else False,
                        'type': 'chat'
                    })
                print(data)
                headers = {'Content-type': 'application/json'}
                request_post = requests.post(url, json=data, headers=headers, verify=False, auth=(
                    self.env.user.login, self.env.user.xmpp_password))
                print(request_post.text)
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
            'channel_partner_ids': [(4, partner_id.id) for partner_id in partner_ids],
            'public': public,
            'channel_type': channel_type
        })
        return channel_id

    def _group_chat(self, vals):
        if "invited" or "declined" in vals.get('text_body'):
            channel_id = self._group_invitation_handler(vals)
        else:
            channel_id = self._group_message_handler(vals)
        return channel_id

    def _group_invitation_handler(self, vals):
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", vals.get("text_body"))
        channel_name = emails[-1].split("@")[0]  # channel alias seems in the last position
        channel_id = self.env[self._name].search([('name', '=', channel_name)])

        partner_user_login = emails[0].split("@")[0]  # the invitee is in the first position
        partner_id = self.env['res.users'].search([('login', '=', partner_user_login)], limit=1).mapped('partner_id')

        if channel_id and partner_id and (partner_id not in channel_id.mapped('channel_partner_ids')) and "invited" in vals.get('text_body'):
            channel_id.write({
                'channel_partner_ids': [(4, partner_id.id)],
            })
        if channel_id and partner_id and (partner_id in channel_id.mapped('channel_partner_ids')) and "declined" in vals.get('text_body'):
            channel_id.write({
                'channel_partner_ids': [(3, partner_id.id)],
            })

        if not channel_id:
            channel_id = self._create_channel(
                channel_name=channel_name,
                partner_ids=[partner_id] if partner_id else False,
                public='groups',
                channel_type='channel'
            )
            channel_id.write({'channel_email': vals.get('sender')})
        return channel_id

    def _group_message_handler(self, contact):
        sender = contact.get('sender').split('/')[1]
        partner_id = self.env['res.users'].search([('login', '=', sender)], limit=1).mapped('partner_id')

        channel_name = contact.get('recipient').split('@')[0]
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
            channel_id.write({'channel_email': contact.get('recipient')})
        print(channel_id.name)
        return channel_id

    def _cleanup_p2p_contact(self, emails):
        cleaned_email = []
        for email in emails:
            cleaned_email.append(email.split('/')[0])
            #email.split('/')
        return cleaned_email

    def _cleanup_group_contact(self, emails):
        cleaned_email = []
        for email in emails:
            cleaned_email.append(email.split('/')[1])  # to='python@chat.lvh.me' from='python@chat.lvh.me/admin'
            #email.split('/')
        return cleaned_email

