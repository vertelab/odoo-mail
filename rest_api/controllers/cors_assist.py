# -*- coding: utf-8 -*-
from .main import *

_logger = logging.getLogger(__name__)


class ControllerREST(http.Controller):
    
    @http.route('/api/<path:path>', methods=['OPTIONS'], type='http', auth='none')
    def api__OPTIONS(self, **kw):
        if rest_cors_value != 'null':
            return werkzeug.wrappers.Response(
                status = 204,
                headers = [
                    ('Access-Control-Allow-Origin', rest_cors_value),
                    ('Access-Control-Allow-Headers', '*'),
                    ('Access-Control-Allow-Methods', '*'),
                ]
            )
