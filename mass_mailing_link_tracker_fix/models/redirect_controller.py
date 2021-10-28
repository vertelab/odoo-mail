import logging
import json
import werkzeug
from odoo import http
from odoo.addons.web.controllers.main import ensure_db
_logger = logging.getLogger(__name__)
class Monitoring(http.Controller):

    @http.route('/mail_statistic', type='http', auth='none')
    def mail_statistic(self, **kwargs):
        _logger.warning("/mail_statistic")
        ensure_db()

        # TODO SAVE STATISTIC
        # SPARA ANTALET KLICKS PER LÄNK

        return werkzeug.utils.redirect('https://' + kwargs.get('url', 'www.arbetsformedlingen.se'), code=307)
