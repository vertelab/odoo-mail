# -*- coding: utf-8 -*-

{
    'name': 'Send mail Nadim',
    'version': '12.0.1.0.1',
    'category': 'other',
    'description': """
Instead of SMTP, this module use RestAPI to send mail between Odoo server and Nadim integration server\n
v12.0.1.0.1 Updated code with fixes\n
""",
    'depends': ['fetchmail'],
    'data': ['security/ir.model.access.csv',
             'views/out_going_server.xml'],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
