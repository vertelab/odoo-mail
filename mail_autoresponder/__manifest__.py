# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Mail Autoresponder',
    'summary': "Adds an automatic Emailing Trigger based service",
    'version': '12.0.0.0.7',
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'maintainer': 'Vertel AB',
    'website': 'http://www.vertel.se',
    'description': """
        - 12.0.0.0.4 
            This version changes calculation to workdays and to send letters to recipients of each \n 
            email each day based on the criteria of the email-line. \n
        - 12.0.0.0.5  Fixed out of range issue \n
        - 12.0.0.0.6  added debuggin \n
    """,
    'depends': [
        'base_setup', 'mail', 'mass_mailing',
        ],
    'data': [
        'security/ir.model.access.csv',
        'data/cron.xml',
        'data/mail_template.xml',
        'views/assets.xml',
        'views/menuitem.xml',
        'views/partner_event_view.xml',
        'views/mail_audit_view.xml',
        'views/mail_template_views.xml',
        'wizard/mail_compose_message_view.xml',
    ],
    'auto_install': False,
    'installable': True,
}
