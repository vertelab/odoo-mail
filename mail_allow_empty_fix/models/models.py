# -*- coding: utf-8 -*-

from odoo import models, fields, api
import lxml
from lxml import etree




class MailThread(models.Model):
    _inherit="mail.thread"


    def _message_extract_payload_postprocess(self, message, body, attachments):

        if not body:
             return body, attachments
        try:
            root = lxml.html.fromstring(body)
        except ValueError:
            # In case the email client sent XHTML, fromstring will fail because 'Unicode strings
            # with encoding declaration are not supported'.
            root = lxml.html.fromstring(body.encode('utf-8'))
        except etree.ParserError:
            body += "<pre></pre>"
        super()._message_extract_payload_postprocess(message, body, attachments)

