# -*- coding: utf-8 -*-
import psycopg2
import base64
import json
import logging
import requests
import uuid
import datetime
import smtplib
import re

from odoo.exceptions import UserError
from odoo.tools import pycompat
from odoo.tools import ustr

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

from odoo import _, api, fields, models
from odoo import tools
from odoo.addons.base.models.ir_mail_server import MailDeliveryException
from odoo.tools.safe_eval import safe_eval

class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    server_type = fields.Selection([
        ('smtp', 'SMTP Server'),
        ('rest', 'Rest API')], 'Server Type',
        default='smtp', required=True)

    client_secret = fields.Char(string='Client Secret')
    client_id = fields.Char(string='Client ID')
    environment = fields.Selection(selection=[('U1', 'U1'),
                                              ('I1', 'I1'),
                                              ('T1', 'T1'),
                                              ('T2', 'T2'),
                                              ('PROD', 'PROD'), ],
                                   string='Environment',
                                   default='T2',
                                   required=True)
    base_url = fields.Char(string='Restful API Url', help="Base URL of API")
    rest_port = fields.Integer(string='Port', default=443)
    resource_type = fields.Selection(string='Resource type',
                                     selection=[('eletter', 'eLetter'), ('email', 'eMail'), ])

    @api.onchange('server_type')
    def check_smtp_information(self):
        if self.server_type == "rest":
            if not self.smtp_host:
                self.smtp_host = "/"
            if not self.smtp_port:
                self.smtp_port = 465
        else:
            if not self.base_url:
                self.base_url = "/"

    def get_headers(self):
        tracking_id = pycompat.text_type(uuid.uuid1())
        headers = {
            'Content-Type': "application/json",
            'AF-TrackingId': tracking_id,
            'AF-EndUserId': "*sys*",
            'AF-SystemId': self.env["ir.config_parameter"].sudo().get_param(
                "api_ipf.ipf_system_id", "AFDAFA"),
            'AF-Environment': self.environment,
        }
        return headers

    @api.multi
    def test_rest_connection(self):
        for server in self:
            try:
                if server.rest_port:
                    url = '{}:{}{}'.format(server.base_url, server.rest_port, '/nadim/emailmessages')
                else:
                    url = '{}{}'.format(server.base_url, '/nadim/emailmessages')

                querystring = {"client_secret": self.client_secret, "client_id": self.client_id}

                response = requests.post(
                    url,
                    headers=self.get_headers(),
                    params=querystring,
                    verify=False)

                if response.status_code:
                    raise UserError(_("Connection Test: %s: %s") % (response.status_code, response.text))
            except UserError as e:
                _logger.info(e)
                raise e
            except Exception as e:
                _logger.info(e)
                raise UserError(_("Connection Test Failed!\n Error: %s") % ustr(e))
        raise UserError(_("Connection Test Succeeded! Everything seems properly set up!"))

    def connect(self, host=None, port=None, user=None, password=None, encryption=None,
                smtp_debug=False, mail_server_id=None):
        if mail_server_id:
            mail_server = self.browse(mail_server_id)
        else:
            domain = []
            mail_server = self.search(domain, limit=1, order='sequence')
        if not mail_server:
            raise UserError(_("Not found any configured server"))

        if mail_server.server_type != 'rest':
            return super(IrMailServer, self).connect(host=host, port=port, user=user, password=password,
                                                     encryption=encryption,
                                                     smtp_debug=smtp_debug, mail_server_id=mail_server_id)
        return None

    def build_email(self, email_from, email_to, subject, body, email_cc=None, email_bcc=None, reply_to=False,
                    attachments=None, message_id=None, references=None, object_id=False, subtype='plain', headers=None,
                    body_alternative=None, subtype_alternative='plain'):
        domain = [('resource_type', '=', self.env.context.get('nadim_type', ''))]
        mail_server = self.search(domain, limit=1, order='sequence')
        if mail_server.server_type != 'rest':
            return super(IrMailServer, self).build_email(email_from, email_to, subject, body, email_cc=email_cc,
                                                         email_bcc=email_bcc, reply_to=reply_to,
                                                         attachments=attachments, message_id=message_id,
                                                         references=references, object_id=object_id, subtype=subtype,
                                                         headers=headers,
                                                         body_alternative=body_alternative,
                                                         subtype_alternative=subtype_alternative)

        body_bytes = body.encode('utf-8')
        base64_bytes = base64.b64encode(body_bytes)
        base64_body = base64_bytes.decode('utf-8')

        if mail_server.resource_type == 'eletter':
            res_id, res_model = object_id.split('-')
            # why does not .browse(res_id) work? 
            res_obj = self.env[res_model].search([('id', '=', res_id)], limit=1)

            res = {
                "externalId": pycompat.text_type(uuid.uuid1()),
                "systemId": "660",  # DAFA
                "subject": subject,
                "body": base64_body,
                "recipientId": res_obj.partner_social_sec_nr.replace('-', ''),
                "zipCode": res_obj.partner_zip,
                "countryCode": res_obj.country_id.code,
                "contentType": "text/html",
                "messageTypeId": "1220",  # eletter
                "messageCategoryId": "1",
                "messagePayloads": [],
            }
        else:
            res = {
                "externalId": pycompat.text_type(uuid.uuid1()),
                "messageTypeId": "1221",  # email
                "systemId": "660",  # DAFA
                "subject": subject,
                "body": base64_body,
                "contentType": "text/html",
                "messageCategoryId": "1",
                "messagePayloads": [],
                "emailAddress": email_to[0],
            }

        for (fname, fcontent, mime) in attachments:
            base64_bytes = base64.b64encode(fcontent)
            base64_fcontent = base64_bytes.decode('utf-8')

            res['messagePayloads'].append(
                {
                    "payload": base64_fcontent,
                    "fileName": fname,
                    "contentType": "application/pdf",
                }
            )

        _logger.debug("NADIM message post: %s" % res)
        return res

    @api.model
    def send_email(self, message, mail_server_id=None, smtp_server=None, smtp_port=None,
                   smtp_user=None, smtp_password=None, smtp_encryption=None, smtp_debug=False,
                   smtp_session=None):
        if mail_server_id:
            mail_server = self.browse(mail_server_id)
        else:
            domain = []
            mail_server = self.search(domain, limit=1, order='sequence')
        if not mail_server:
            raise UserError(_("Not found any configured server"))
        if type(message) != dict:
            return
        if mail_server.server_type != 'rest':
            return super(IrMailServer, self).send_email(message, mail_server_id=mail_server_id, smtp_server=smtp_server,
                                                        smtp_port=smtp_port,
                                                        smtp_user=smtp_user, smtp_password=smtp_password,
                                                        smtp_encryption=smtp_encryption, smtp_debug=smtp_debug,
                                                        smtp_session=smtp_session)

        return mail_server.restapi_email_post_request(message)

    def restapi_email_post_request(self, datas):
        if self.resource_type == 'eletter':
            resource_path = '/nadim/elettermessages'
        else:
            resource_path = '/nadim/emailmessages'

        if self.rest_port:
            url = '{}:{}{}'.format(self.base_url, self.rest_port, resource_path)
        else:
            url = '{}{}'.format(self.base_url, resource_path)

        querystring = {
            "client_secret": self.client_secret,
            "client_id": self.client_id
        }

        try:
            response = requests.post(url=url, params=querystring, data=json.dumps(datas), headers=self.get_headers(),
                                     verify=False)
            _logger.warning("NADIM response: %s" % response.text)
            if response.status_code != 200:
                raise UserError(_("Mail send failed! Something went wrong!"))
        except UserError as e:
            _logger.info(e)
            raise e
        except Exception as e:
            _logger.info(e)
            raise UserError(_("Mail sending failed! Here is what we got instead:\n %s") % ustr(e))


class MailMail(models.Model):
    _inherit = 'mail.mail'

    @api.multi
    def send(self, auto_commit=False, raise_exception=False):
        """ Sends the selected emails immediately, ignoring their current
            state (mails that have already been sent should not be passed
            unless they should actually be re-sent).
            Emails successfully delivered are marked as 'sent', and those
            that fail to be deliver are marked as 'exception', and the
            corresponding error mail is output in the server logs.

            :param bool auto_commit: whether to force a commit of the mail status
                after sending each mail (meant only for scheduler processing);
                should never be True during normal transactions (default: False)
            :param bool raise_exception: whether to raise an exception if the
                email sending process has failed
            :return: True
        """
        for server_id, batch_ids in self._split_by_server():
            smtp_session = None
            try:
                smtp_session = self.env['ir.mail_server'].connect(mail_server_id=server_id)
            except Exception as exc:
                if raise_exception:
                    # To be consistent and backward compatible with mail_mail.send() raised
                    # exceptions, it is encapsulated into an Odoo MailDeliveryException
                    _logger.error(_('Unable to connect to SMTP Server %s' % str(exc)))
                    raise MailDeliveryException(_('Unable to connect to SMTP Server'), exc)
                else:
                    batch = self.browse(batch_ids)
                    batch.write({'state': 'exception', 'failure_reason': exc})
                    _logger.error(_("Error on sending mail '%s'. %s" % (self.subject, str(exc))))
                    batch._postprocess_sent_message(success_pids=[], failure_type="SMTP")
            else:
                self.browse(batch_ids)._send(
                    auto_commit=auto_commit,
                    raise_exception=raise_exception,
                    smtp_session=smtp_session)
                _logger.info(
                    'Sent batch %s emails via mail server ID #%s',
                    len(batch_ids), server_id)
            finally:
                if smtp_session:
                    smtp_session.quit()

    @api.multi
    def _send(self, auto_commit=False, raise_exception=False, smtp_session=None):
        IrMailServer = self.env['ir.mail_server']
        IrAttachment = self.env['ir.attachment']
        for mail_id in self.ids:
            success_pids = []
            failure_type = None
            processing_pid = None
            mail = None
            try:
                mail = self.browse(mail_id)
                if mail.state != 'outgoing':
                    if mail.state != 'exception' and mail.auto_delete:
                        mail.sudo().unlink()
                    continue

                # remove attachments if user send the link with the access_token
                body = mail.body_html or ''
                attachments = mail.attachment_ids
                for link in re.findall(r'/web/(?:content|image)/([0-9]+)', body):
                    attachments = attachments - IrAttachment.browse(int(link))

                # load attachment binary data with a separate read(), as prefetching all
                # `datas` (binary field) could bloat the browse cache, triggerring
                # soft/hard mem limits with temporary data.
                attachments = [(a['datas_fname'], base64.b64decode(a['datas']), a['mimetype'])
                               for a in attachments.sudo().read(['datas_fname', 'datas', 'mimetype']) if
                               a['datas'] is not False]

                # specific behavior to customize the send email for notified partners
                email_list = []
                if mail.email_to:
                    email_list.append(mail._send_prepare_values())
                for partner in mail.recipient_ids:
                    values = mail._send_prepare_values(partner=partner)
                    values['partner_id'] = partner
                    email_list.append(values)

                # headers
                headers = {}
                ICP = self.env['ir.config_parameter'].sudo()
                bounce_alias = ICP.get_param("mail.bounce.alias")
                catchall_domain = ICP.get_param("mail.catchall.domain")
                if bounce_alias and catchall_domain:
                    if mail.model and mail.res_id:
                        headers['Return-Path'] = '%s+%d-%s-%d@%s' % (
                            bounce_alias, mail.id, mail.model, mail.res_id, catchall_domain)
                    else:
                        headers['Return-Path'] = '%s+%d@%s' % (bounce_alias, mail.id, catchall_domain)
                if mail.headers:
                    try:
                        headers.update(safe_eval(mail.headers))
                    except Exception:
                        pass

                # Writing on the mail object may fail (e.g. lock on user) which
                # would trigger a rollback *after* actually sending the email.
                # To avoid sending twice the same email, provoke the failure earlier
                mail.write({
                    'state': 'exception',
                    'failure_reason': _(
                        'Error without exception. Probably due do sending an email without computed recipients.'),
                })
                _logger.error(_(
                    "Error on sending mail '%s'. Error without exception. Probably due do sending an email without "
                    "computed recipients." % mail.subject))
                # Update notification in a transient exception state to avoid concurrent
                # update in case an email bounces while sending all emails related to current
                # mail record.
                notifs = self.env['mail.notification'].search([
                    ('is_email', '=', True),
                    ('mail_id', 'in', mail.ids),
                    ('email_status', 'not in', ('sent', 'canceled'))
                ])
                if notifs:
                    notif_msg = _(
                        'Error without exception. Probably due do concurrent access update of notification records. Please see with an administrator.')
                    notifs.sudo().write({
                        'email_status': 'exception',
                        'failure_type': 'UNKNOWN',
                        'failure_reason': notif_msg,
                    })

                # build an RFC2822 email.message.Message object and send it without queuing
                res = None
                for email in email_list:
                    msg = IrMailServer.build_email(
                        email_from=mail.email_from,
                        email_to=email.get('email_to'),
                        subject=mail.subject,
                        body=email.get('body'),
                        body_alternative=email.get('body_alternative'),
                        email_cc=tools.email_split(mail.email_cc),
                        reply_to=mail.reply_to,
                        attachments=attachments,
                        message_id=mail.message_id,
                        references=mail.references,
                        object_id=mail.res_id and ('%s-%s' % (mail.res_id, mail.model)),
                        subtype='html',
                        subtype_alternative='plain',
                        headers=headers)
                    processing_pid = email.pop("partner_id", None)
                    try:
                        res = IrMailServer.send_email(
                            msg, mail_server_id=mail.mail_server_id.id, smtp_session=smtp_session)
                        if processing_pid:
                            success_pids.append(processing_pid)
                        processing_pid = None
                    except AssertionError as error:
                        if str(error) == IrMailServer.NO_VALID_RECIPIENT:
                            failure_type = "RECIPIENT"
                            # No valid recipient found for this particular
                            # mail item -> ignore error to avoid blocking
                            # delivery to next recipients, if any. If this is
                            # the only recipient, the mail will show as failed.
                            _logger.info("Ignoring invalid recipients for mail.mail %s: %s",
                                         mail.message_id, email.get('email_to'))
                        else:
                            raise
                if res:  # mail has been sent at least once, no major exception occured
                    mail.write({'state': 'sent', 'message_id': res, 'failure_reason': False})
                    _logger.info('Mail with ID %r and Message-Id %r successfully sent', mail.id, mail.message_id)
                    # /!\ can't use mail.state here, as mail.refresh() will cause an error
                    # see revid:odo@openerp.com-20120622152536-42b2s28lvdv3odyr in 6.1
                mail._postprocess_sent_message(success_pids=success_pids, failure_type=failure_type)
            except MemoryError:
                # prevent catching transient MemoryErrors, bubble up to notify user or abort cron job
                # instead of marking the mail as failed
                _logger.exception(
                    'MemoryError while processing mail with ID %r and Msg-Id %r. Consider raising the --limit-memory-hard startup option',
                    mail.id, mail.message_id)
                # mail status will stay on ongoing since transaction will be rollback
                raise
            except (psycopg2.Error, smtplib.SMTPServerDisconnected):
                # If an error with the database or SMTP session occurs, chances are that the cursor
                # or SMTP session are unusable, causing further errors when trying to save the state.
                _logger.exception(
                    'Exception while processing mail with ID %r and Msg-Id %r.',
                    mail.id, mail.message_id)
                raise
            except Exception as e:
                failure_reason = tools.ustr(e)
                _logger.error('failed sending mail (id: %s) due to %s', mail.id, failure_reason)
                mail.write({'state': 'exception', 'failure_reason': failure_reason})
                mail._postprocess_sent_message(success_pids=success_pids, failure_reason=failure_reason,
                                               failure_type='UNKNOWN')
                if raise_exception:
                    if isinstance(e, (AssertionError, UnicodeEncodeError)):
                        if isinstance(e, UnicodeEncodeError):
                            value = "Invalid text: %s" % e.object
                        else:
                            # get the args of the original error, wrap into a value and throw a MailDeliveryException
                            # that is an except_orm, with name and value as arguments
                            value = '. '.join(e.args)
                        raise MailDeliveryException(_("Mail Delivery Failed"), value)
                    raise

            if auto_commit is True:
                self._cr.commit()
        return True
