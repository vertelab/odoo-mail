from distutils.util import change_root
import logging
import requests
import odoorpc

from ntpath import join
from xml.dom import ValidationErr
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


# class MessagePost(models.Model):
#     _name = "message.post.test"
#     _inherit = ["mail.thread"]
#
#     @api.model
#     def message_post_test(self, *args):
#         for arg in args:
#             if channel := self.env["mail.channel"].browse(arg.get('id')):
#                 _logger.error(f"{channel=}")
#                 new_arg = {a: arg[a] for a in arg}
#                 new_arg["prosody"] = True
#                 message_post = channel.message_post(**new_arg).id
#                 return message_post
