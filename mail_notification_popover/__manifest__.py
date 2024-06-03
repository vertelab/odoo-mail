{
    'name': 'Mail: Notification Popover',
    'version': '14.0.0.0.0',
    'summary': 'Odoo Mail.',
    'category': 'Administration',
    'description': """"
        Adds partner email to mail notification popover.
    """,
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-mail/mail_notification_popover',
    'images': ['static/description/banner.png'],  # 560x280 px.
    'license': 'AGPL-3',
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-mail',
    'depends': ['mail'],
    'data': [],
    'qweb': [
        'static/src/xml/notification_popover.xml',
    ],
}
