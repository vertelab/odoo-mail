# -*- coding: utf-8 -*-
from email import encoders
from email.mime.base import MIMEBase
import requests
import json
import datetime
import logging
from odoo.tools import pycompat
import uuid

from odoo import api, fields, models, tools, _
from odoo.exceptions import except_orm, UserError
from odoo.tools import ustr

_logger = logging.getLogger(__name__)


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    server_type = fields.Selection([
        ('smtp', 'SMTP Server'),
        ('rest', 'Rest API')], 'Server Type',
        default='smtp', required=True)

    client_secret = fields.Char(string='Client Secret',
                                required=True)
    client_id = fields.Char(string='Client ID',
                            required=True)
    environment = fields.Selection(selection=[('U1', 'U1'),
                                              ('I1', 'I1'),
                                              ('T1', 'IT'),
                                              ('T2', 'T2'),
                                              ('PROD', 'PROD'), ],
                                   string='Environment',
                                   default='T2',
                                   required=True)
    base_url = fields.Char(string='Restful API Url', help="Base URL of API")
    rest_port = fields.Integer(string='Port', default=5000)
    resource_path = fields.Char()

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
            if not self.resource_path:
                self.resource_path = "/"

    def get_headers(self):
        tracking_id = pycompat.text_type(uuid.uuid1())
        headers = {
            'x-amf-mediaType': "application/json",
            'AF-TrackingId': tracking_id,
            'AF-SystemId': "AF-SystemId",
            'AF-EndUserId': "AF-EndUserId",
            'AF-Environment': self.environment,
        }
        return headers

    @api.multi
    def test_rest_connection(self):
        for server in self:
            try:
                if server.rest_port:
                    url = '{}:{}{}'.format(server.base_url, server.rest_port, server.resource_path)
                else:
                    url = '{}{}'.format(server.base_url, server.resource_path)

                querystring = {"client_secret": self.client_secret,
                       "client_id": self.client_id}

                response = requests.get(
                    url,
                    headers=self.get_headers(),
                    params=querystring,
                    verify=False)

                if response.status_code != 200:
                    raise UserError(_("Connection Test Failed! Can't connect to server!"))
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
        domain = []
        mail_server = self.search(domain, limit=1, order='sequence')
        if mail_server.server_type != 'rest':
            return super(IrMailServer, self).build_email(email_from, email_to, subject, body, email_cc=email_cc,
                                                         email_bcc=email_bcc, reply_to=reply_to,
                                                         attachments=attachments, message_id=message_id,
                                                         references=references, object_id=object_id, subtype=subtype,
                                                         headers=headers,
                                                         body_alternative=body_alternative,
                                                         subtype_alternative=subtype_alternative)

        emailAddresses = []
        if email_cc:
            emailAddresses.extend(email_cc.split(","))
        if email_bcc:
            emailAddresses.extend(email_bcc.split(","))

        res = {
            "recipientId": "{}{}".format(datetime.datetime.now().strftime("%Y%m%d"), message_id),
            "externalId": message_id,
            "messageTypeId": "1",
            "systemId": "1",
            "subject": subject,
            "body": body,
            "contentType": "text/html",
            "messageCategoryId": "1",
            "messagePayloads": [],
            "emailAddresses": emailAddresses,
            "emailAddress": email_to,
        }

        for (fname, fcontent, mime) in attachments:
            if mime and '/' in mime:
                maintype, subtype = mime.split('/', 1)
                part = MIMEBase(maintype, subtype)
            else:
                part = MIMEBase('application', "octet-stream")
            part.set_payload(fcontent)
            encoders.encode_base64(part)

            res['messagePayloads'].append(
                {
                    "payload": str(part),
                    "fileName": fname,
                    "contentType": mime,
                }
            )
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
        if mail_server.server_type != 'rest':
            return super(IrMailServer, self).send_email(message, mail_server_id=mail_server_id, smtp_server=smtp_server,
                                                        smtp_port=smtp_port,
                                                        smtp_user=smtp_user, smtp_password=smtp_password,
                                                        smtp_encryption=smtp_encryption, smtp_debug=smtp_debug,
                                                        smtp_session=smtp_session)

        return mail_server.restapi_email_post_request(message)

    def restapi_email_post_request(self, datas):
        if self.rest_port:
            url = '{}:{}{}'.format(self.base_url, self.rest_port, self.resource_path)
        else:
            url = '{}{}'.format(self.base_url, self.resource_path)

        headers = {'content-type': 'application/json'}
        try:
            response = requests.post(url=url, data=json.dumps(datas), headers=headers)
            if response.status_code != 200:
                raise UserError(_("Mail send failed! Something went wrong!"))
        except UserError as e:
            _logger.info(e)
            raise e
        except Exception as e:
            _logger.info(e)
            raise UserError(_("Mail sending failed! Here is what we got instead:\n %s") % ustr(e))
