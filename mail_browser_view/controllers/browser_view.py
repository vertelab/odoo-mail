# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import http
from odoo.http import request

class EmailBrowserViewController(http.Controller):

    @http.route(['/email/view/<string:token>'],
                type='http', auth='public', website=True)
    def email_view(self, token, **kwargs):
        record = request.env['mail.mail'].get_record_for_token(token)
        if not record:
            return request.not_found()
        if len(record.recipient_ids) == 1:
            unsubscribe_url = record._get_unsubscribe_url(
                record.recipient_ids.email)
            base_url = http.request.env['ir.config_parameter'].sudo().get_param(
                'web.base.url').rstrip('/')
            link_to_replace = base_url + '/unsubscribe_from_list'
            if link_to_replace in record['body']:
                record['body'] = record['body'].replace(link_to_replace,
                                                        unsubscribe_url
                                                        if unsubscribe_url
                                                        else '#')
        record._add_title()
        return request.make_response(record.body_html)
