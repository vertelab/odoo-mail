# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2019 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import datetime
import logging
import poplib
from imaplib import IMAP4, IMAP4_SSL
from odoo.exceptions import UserError
from poplib import POP3, POP3_SSL

from odoo import api, fields, models, tools, _

_logger = logging.getLogger(__name__)
MAX_POP_MESSAGES = 50
MAIL_TIMEOUT = 60

# Workaround for Python 2.7.8 bug https://bugs.python.org/issue23906
poplib._MAXLINE = 65536


class FetchmailServerProcessed(models.Model):
    _name = 'fetchmail.server.processed'
    _description = "Fetchmail Server Processed"

    msg_id = fields.Integer(string='Message id')

    @api.multi
    def cleanup(self, days=7):
        """ cron job to remove old entries after X days"""
        old_messages = self.search(
            [('created', '<', (datetime.datetime.now() - datetime.timedelta(days=days)).strftime('%d-%m-%Y'))])
        for msg in old_messages:
            msg.unlink()


class FetchmailServer(models.Model):
    """Incoming POP/IMAP mail server account"""
    _inherit = 'fetchmail.server'

    @api.multi
    def fetch_mail(self):
        """ WARNING: meant for cron usage only - will commit() after each email! """
        additionnal_context = {
            'fetchmail_cron_running': True
        }
        MailThread = self.env['mail.thread']
        for server in self:
            _logger.info('start checking for new emails on %s server %s', server.type, server.name)
            additionnal_context['fetchmail_server_id'] = server.id
            additionnal_context['server_type'] = server.type
            count, failed = 0, 0
            imap_server = None
            pop_server = None
            if server.type == 'imap':
                try:
                    imap_server = server.connect()
                    # readonly to make sure we don't change any mails
                    imap_server.select(readonly=True)
                    # Check only emails for the past 3 days instead of checking unseen mails
                    result, data = imap_server.search(None, '(SINCE "%s")' % (
                                datetime.datetime.now() - datetime.timedelta(days=3)).strftime('%d-%b-%Y'))
                    for num in data[0].split():
                        res_id = None
                        # check if message has already been processed
                        if not self.env['fetchmail.server.processed'].search([('msg_id', '=', num)]):
                            result, data = imap_server.fetch(num, '(RFC822)')
                            try:
                                # save a record of having processed the message
                                self.env['fetchmail.server.processed'].create({'msg_id': num})
                                res_id = MailThread.with_context(**additionnal_context).message_process(
                                    server.object_id.model, data[0][1], save_original=server.original,
                                    strip_attachments=(not server.attach))
                            except Exception:
                                _logger.info('Failed to process mail from %s server %s.', server.type, server.name,
                                             exc_info=True)
                                failed += 1
                            if res_id and server.action_id:
                                server.action_id.with_context({
                                    'active_id': res_id,
                                    'active_ids': [res_id],
                                    'active_model': self.env.context.get("thread_model", server.object_id.model)
                                }).run()
                            self._cr.commit()
                            count += 1
                    _logger.info("Fetched %d email(s) on %s server %s; %d succeeded, %d failed.", count, server.type,
                                 server.name, (count - failed), failed)
                except Exception:
                    _logger.info("General failure when trying to fetch mail from %s server %s.", server.type,
                                 server.name, exc_info=True)
                finally:
                    if imap_server:
                        imap_server.close()
                        imap_server.logout()
            elif server.type == 'pop':
                # NOT CHANGED!
                # NOT SUPPORTED !
                try:
                    while True:
                        pop_server = server.connect()
                        (num_messages, total_size) = pop_server.stat()
                        pop_server.list()
                        for num in range(1, min(MAX_POP_MESSAGES, num_messages) + 1):
                            (header, messages, octets) = pop_server.retr(num)
                            message = '\n'.join(messages)
                            res_id = None
                            try:
                                res_id = MailThread.with_context(**additionnal_context).message_process(
                                    server.object_id.model, message, save_original=server.original,
                                    strip_attachments=(not server.attach))
                                pop_server.dele(num)
                            except Exception:
                                _logger.info('Failed to process mail from %s server %s.', server.type, server.name,
                                             exc_info=True)
                                failed += 1
                            if res_id and server.action_id:
                                server.action_id.with_context({
                                    'active_id': res_id,
                                    'active_ids': [res_id],
                                    'active_model': self.env.context.get("thread_model", server.object_id.model)
                                }).run()
                            self.env.cr.commit()
                        if num_messages < MAX_POP_MESSAGES:
                            break
                        pop_server.quit()
                        _logger.info("Fetched %d email(s) on %s server %s; %d succeeded, %d failed.", num_messages,
                                     server.type, server.name, (num_messages - failed), failed)
                except Exception:
                    _logger.info("General failure when trying to fetch mail from %s server %s.", server.type,
                                 server.name, exc_info=True)
                finally:
                    if pop_server:
                        pop_server.quit()
            server.write({'date': fields.Datetime.now()})
        return True
