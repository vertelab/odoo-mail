from distutils.util import change_root
import logging
import requests
import odoorpc

from ntpath import join
from xml.dom import ValidationErr
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)

class ChannelSearchRead(models.Model):
    _inherit = "mail.channel"

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
    def message_post(self, *,
                     body='', subject=None, message_type='notification',
                     email_from=None, author_id=None, parent_id=False,
                     subtype_xmlid=None, subtype_id=False, partner_ids=None, channel_ids=None,
                     attachments=None, attachment_ids=None,
                     add_sign=True, record_name=False,
                     **kwargs):

                    #_logger.error(f"{kwargs=}")

                    res = super().message_post(body=body, subject=subject, message_type=message_type,
                                                email_from=email_from, author_id=author_id, parent_id=parent_id,
                                                subtype_xmlid=subtype_xmlid, subtype_id=subtype_id, partner_ids=partner_ids,
                                                channel_ids=channel_ids, attachments=attachments, attachment_ids=attachment_ids,
                                                add_sign=add_sign, record_name=record_name, **kwargs)
                    #_logger.error(f"res {res=}")
                    if res.id and not kwargs.get("prosody"):
                        url = "https://hoary.vertel.se:5281/rest"
                        js = {'body': body, 'kind': 'message', 'to': 'dostoevsky@hoary.vertel.se', 
                              'type': 'chat', 'id': 'ODOOODOO' + str(res.id)}
                        headers = {'Content-type': 'application/json'}
                        request_post = requests.post(url, json=js, headers=headers, verify=False, auth=("admin", "admin"))
                    return res