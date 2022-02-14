# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class EmailBrowserViewController(http.Controller):

    @http.route(['/email/view/<string:token>'],
                type='http', auth='public', website=True)
    def email_view(self, token, **kwargs):
        record = request.env['mail.mail'].get_record_for_token(token)
        if not record:
            return request.not_found()
        body = record._send_prepare_body()
        email = record.email_to
        if email:
            unsubscribe_url = record._get_unsubscribe_url(email)
            base_url = http.request.env['ir.config_parameter'].sudo().get_param(
                'web.base.url').rstrip('/')
            link_to_replace = base_url + '/unsubscribe_from_list'
            if link_to_replace in body:
                body = body.replace(link_to_replace,
                                    unsubscribe_url
                                    if unsubscribe_url
                                    else '#')
        body = record._add_title(body)
        return request.make_response(body)
