# -*- coding: utf-8 -*-

{
    'name': 'Send mail Nadim',
    'version': '1.0',
    'category': 'other',
    'description': """
Instead of SMTP, this module use RestAPI to send mail between Odoo server and Nadim integration server
""",
    'depends': ['fetchmail'],
    'data': ['security/ir.model.access.csv',
             'views/out_going_server.xml'],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
