from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError
from odoo import tools
import uuid
import re
from email.message import Message
import logging
import base64
import datetime
import dateutil
import email
import hashlib
import hmac
import lxml
import logging
import pytz
import re
import socket
import time
import re
try:
    from xmlrpc import client as xmlrpclib
except ImportError:
    import xmlrpclib
from collections import namedtuple
from email.message import Message
from lxml import etree
from werkzeug import url_encode
from werkzeug import urls
from odoo import _, api, exceptions, fields, models, tools
from odoo.tools import pycompat, ustr, formataddr
from odoo.tools.misc import clean_context
from odoo.tools.safe_eval import safe_eval
_logger = logging.getLogger(__name__)

class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'
    @api.multi
    def message_receive_bounce(self, email, partner, mail_id=None):
        """Called by ``message_process`` when a bounce email (such as Undelivered
        Mail Returned to Sender) is received for an existing thread. The default
        behavior is to check is an integer  ``message_bounce`` column exists.
        If it is the case, its content is incremented.
        :param mail_id: ID of the sent email that bounced. It may not exist anymore
                        but it could be usefull if the information was kept. This is
                        used notably in mass mailing.
        :param RecordSet partner: partner matching the bounced email address, if any
        :param string email: email that caused the bounce """
        if 'message_bounce' in self._fields:
            for record in self:
                message = self.env.context.get('message', False)
                if message:
                    code = message._payload[1]._payload[1]._headers[3][1]
                    description = message._payload[1]._payload[1]._headers[-1][1]
                    found = False
                    for category in record.bouncing_categories:
                        if category.code == code and category.description == description:
                            category.bounces = category.bounces + 1
                            found = True
                    if not found:
                        bounce_category = self.env['mail.bounce.category'].create({'bounces': 1, 'code': code, 'mailing_contact': record.id, 'description':description})
                        # record.write({'bouncing_categories': [(0, 0, {'bounces': 1, 'code': code})]})
                record.message_bounce = record.message_bounce + 1
    @api.model
    def message_route(self, message, message_dict, model=None, thread_id=None, custom_values=None):
        """ Override to udpate mass mailing statistics based on bounce emails """
        context_copy = self.env.context.copy()
        context_copy.update({'message': message})
        self.env.context = context_copy
        return super(MailThread, self.with_context(context_copy)).message_route(message, message_dict, model, thread_id, custom_values)
        # ~ message._payload[1]._payload[1]._headers[-1]
class MassMailingContact(models.AbstractModel):
    _inherit = 'mail.mass_mailing.contact'
    bouncing_categories = fields.One2many(comodel_name='mail.bounce.category', inverse_name='mailing_contact', string='')
    @api.multi
    def action_bounce_categories_tree_view(self):
        tree_view_id = self.env.ref('mass_mailing_bouncing_categories.view_categories_tree').id
        return {
            'name': _('Bouncing Categories'),
            'type': 'ir.actions.act_window',
            'res_model': 'mail.bounce.category',
            'view_type': 'form',
            'view_mode': 'tree',
            'domain': [('id', 'in', self.bouncing_categories.mapped('id'))],
            'view_id': tree_view_id,
            'res_id': False,
            'context': False,
            'target': 'new',
        }
class MassMailingBounceCategories(models.Model):
    _name = 'mail.bounce.category'
    mailing_contact = fields.Many2one(comodel_name='mail.mass_mailing.contact', string='')
    bounces = fields.Integer(string='')
    code = fields.Char(string='')
    description = fields.Char(string='')





















