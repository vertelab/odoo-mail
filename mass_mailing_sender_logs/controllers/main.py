import logging
import json
from odoo import models, api, _, http
import base64
import werkzeug
from odoo import _, exceptions, http
from odoo.http import request
from odoo.tools import consteq
import werkzeug
import os
import logging
_logger = logging.getLogger(__name__)

from odoo.addons.mass_mailing.controllers.main import MassMailController

class PerMailMassMailController(MassMailController):
    @http.route('/r/<string:code>/m/<int:stat_id>', type='http', auth="none")
    def full_url_redirect(self, code, stat_id, **post):
        # don't assume geoip is set, it is part of the website module
        # which mass_mailing doesn't depend on
        country_code = request.session.get('geoip', False) and request.session.geoip.get('country_code', False)
        request.env['link.tracker.click'].add_click(code, request.httprequest.remote_addr, country_code, stat_id=stat_id)
        return werkzeug.utils.redirect(request.env['link.tracker'].get_url_from_code(code), 307)
    
