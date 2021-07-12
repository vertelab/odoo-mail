# -*- coding: utf-8 -*-

{
    'name': 'Send mail Nadim',
    'version': '12.0.1.0.4',
    'category': 'Mail',
    'author': 'Arbetsförmedlingen',
    'website': 'https://arbetsformedlingen.se/',
    'summary': """
Instead of SMTP, this module use RestAPI to send messages between Odoo server and Nadim integration server.
""",
    'description': """
    Instead of SMTP, this module use RestAPI to send messages between Odoo server and Nadim integration server. \n
    
    v12.0.1.0.4 - Added logger for Failed email.
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
