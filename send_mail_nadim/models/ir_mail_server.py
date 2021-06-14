# -*- coding: utf-8 -*-
import base64
import json
import logging
import requests
import uuid
from odoo.exceptions import UserError
from odoo.tools import pycompat
from odoo.tools import ustr

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


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
