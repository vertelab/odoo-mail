# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Mail Autoresponder',
    'summary': "Adds an automatic Emailing Trigger based service",
    'version': '12.0.2.4.7',
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'maintainer': 'Vertel AB',
    'website': 'http://www.vertel.se',
    'description': """
        V12.0.0.0.4 
            This version changes calculation to workdays and to send letters to recipients of each.\n
            email each day based on the criteria of the email-line.\n
        V12.0.0.0.5  Fixed out of range issue.\n
        V12.0.0.0.6  added debuggin.\n
        V12.0.1.0.9  Updates on sending logic.\n
        V12.0.2.0.0  Changed access right for autoresponder menu.\n
        v12.0.2.1.0  Added translation to mass_mailing_autoresponder.\n
        v12.0.2.1.1  Add translation to template name in autoresponder.\n
        v12.0.2.2.0  Added weekdays and holidays filtering.\n
        v12.0.2.2.1  Add translation to template name in autoresponder.\n
        v12.0.2.3.0  AFC-2732 Adjust access right for email marketing user.\n
        v12.0.2.3.1  AFC-3027 Adjust access right for ADKD manual user.\n
        v12.0.2.4.0  AFC-3028 Created new access group ADKD manual guest and adjusted access right.\n
        v12.0.2.4.1  AFC-3159 Hide create and import button for ADKD guest group.\n
        v12.0.2.4.2  AFC-3170 Hide button for ADKD guest group.\n
        v12.0.2.4.3  AFC-3146 Hide import button for all users.\n
        v12.0.2.4.4  AFC-3351 Hide actions dropdown menu for ADKD guest group.\n
        v12.0.2.4.5  AFC-3103 Autoresponder doesnt create a mass_mailing per contact anymore.\n
        v12.0.2.4.6  AFC-3528 Added translation.\n
        v12.0.2.4.6  AFC-3529 Fixed typo in translation.\n
    """,
    'depends': [
        'base_setup', 'mail', 'mass_mailing', 'resource', 'af_security',
        ],
    'data': [
        'security/ir.model.access.csv',
        'data/cron.xml',
        'data/mail_template.xml',
        'views/assets.xml',
        'views/menuitem.xml',
        'views/partner_event_view.xml',
        'views/mass_mailing_view.xml',
        'views/mail_audit_view.xml',
        'views/mail_template_views.xml',
        'wizard/mail_compose_message_view.xml',
    ],
    'qweb': ['static/src/xml/base_import.xml'],
    'auto_install': False,
    'installable': True,
}
