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

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
import datetime

import logging
_logger = logging.getLogger(__name__)
MAX_POP_MESSAGES = 50
MAIL_TIMEOUT = 60



class FetchmailServerProcessed(models.Model):
    _name = 'fetchmail.server.processed'

    msg_id = fields.Integer(string='Message id')

    @api.multi
    def cleanup(self, days=7):
        """ cron job to remove old entries after X days"""
        old_messages = self.search([('created','<',(datetime.datetime.now() - datetime.timedelta(days=days)).strftime('%d-%m-%Y'))])
        for msg in old_messages:
            msg.unlink()

class FetchmailServer(models.Model):
    """Incoming POP/IMAP/NADIM mail server account"""
    _inherit = 'fetchmail.server'


    @api.multi
    def nadim_connect(self):
        pass
        
    @api.multi
    def nadim_search(self):
        pass

    @api.multi
    def nadim_fetch(self):
        pass


    @api.multi
    def nadim_close(self):
        pass


    @api.multi
    def fetch_mail(self):
        """ WARNING: meant for cron usage only - will commit() after each email! """
        additionnal_context = {
            'fetchmail_cron_running': True
        }
        super(FetchmailServer,self).fetch_mail()
        MailThread = self.env['mail.thread']
        for server in self:
            _logger.info('start checking for new emails on %s server %s', server.type, server.name)
            additionnal_context['fetchmail_server_id'] = server.id
            additionnal_context['server_type'] = server.type
            count, failed = 0, 0
            if server.type == 'nadim':
                try:
                    nadim_server = server.nadim_connect()
                    # readonly to make sure we don't change any mails
                    nadim_server.nadim_select(readonly=True)
                    # Check only emails for the past 3 days instead of checking unseen mails
                    result, data = imap_server.nadim_search(None, '(SINCE "%s")' % (datetime.datetime.now() - datetime.timedelta(days=3)).strftime('%d-%b-%Y'))
                    for num in data[0].split():
                        res_id = None
                        # check if message has already been processed
                        if not self.env['fetchmail.server.processed'].search([('msg_id','=',num)]):
                            result, data = imap_server.nadim_fetch(num, '(RFC822)')
                            try:
                                # save a record of having processed the message
                                self.env['fetchmail.server.processed'].create({'msg_id': num})
                                res_id = MailThread.with_context(**additionnal_context).message_process(server.object_id.model, data[0][1], save_original=server.original, strip_attachments=(not server.attach))
                            except Exception:
                                _logger.info('Failed to process mail from %s server %s.', server.type, server.name, exc_info=True)
                                failed += 1
                            if res_id and server.action_id:
                                server.action_id.with_context({
                                    'active_id': res_id,
                                    'active_ids': [res_id],
                                    'active_model': self.env.context.get("thread_model", server.object_id.model)
                                }).run()
                            self._cr.commit()
                            count += 1
                    _logger.info("Fetched %d email(s) on %s server %s; %d succeeded, %d failed.", count, server.type, server.name, (count - failed), failed)
                except Exception:
                    _logger.info("General failure when trying to fetch mail from %s server %s.", server.type, server.name, exc_info=True)
                finally:
                    if nadim_server:
                        imap_server.nadim_close()
            server.write({'date': fields.Datetime.now()})
            
        return True