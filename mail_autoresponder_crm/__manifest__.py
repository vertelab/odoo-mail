# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Mail Autoresponder CRM',
    'summary': "Adds an automatic emailing trigger based service",
    'version': '12.0.0.0.2',
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'maintainer': 'Vertel AB',
    'website': 'http://www.vertel.se',
    'depends': ['base_setup', 'mail', 'mail_autoresponder', 'partner_daily_notes'],
    'data': [
        'views/partner_event_view.xml',

    ],
    'auto_install': False,
    'installable': True,
}