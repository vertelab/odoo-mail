# -*- coding: utf-8 -*-

from odoo import models, fields, api
import lxml
from lxml import etree
import logging
_logger = logging.getLogger(__name__)



class MailThread(models.AbstractModel):
    _inherit="mail.thread"


    def _message_extract_payload_postprocess(self, message, body, attachments):

        if not body:
             return body, attachments
        try:
            root = lxml.html.fromstring(body)
        except etree.ParserError:
            return " ", attachments
        super()._message_extract_payload_postprocess(message, body, attachments)

