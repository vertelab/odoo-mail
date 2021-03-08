# -*- coding: utf-8 -*-

{
    'name': 'Send mail Nadim',
    'version': '12.0.1.0.3',
    'category': 'Mail',
    'author':   'Arbetsförmedlingen',
    'website':  'https://arbetsformedlingen.se/',
    'summary': """
Instead of SMTP, this module use RestAPI to send messages between Odoo server and Nadim integration server.
""",
    'depends': ['fetchmail'],
    'data': ['security/ir.model.access.csv',
             'views/out_going_server.xml',
             "data/ir.mail_server.csv",
             ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
