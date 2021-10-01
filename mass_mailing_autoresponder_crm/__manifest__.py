# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Mail Autoresponder CRM',
    'summary': "Adds an automatic emailing trigger based service",
    'version': '12.0.1.0.7',
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'maintainer': 'Vertel AB',
    'description': """
        - 12.0.1.0.4  Changed user-groups to menu \n
        - 12.0.1.0.5  AFC-2341 Added user-role to the 'Email Marketing'' to prevent it to be visible for users outside 
        of the Newsletter-Manual-group\n
        - 12.0.1.0.6  AFC-2117 Added new model for adkd campaign, added m2m adkd campaign field to res_partner \n
        - 12.0.1.0.7 AFC-2817 Removed incorrect linebreak \n 
    """,
    'website': 'http://www.vertel.se',
    'depends': ['base_setup', 'mail', 'mass_mailing_autoresponder', 'partner_daily_notes', 'af_security'
                ],
    'data': [
        'views/partner_event_view.xml',
        'security/ir.model.access.csv'
    ],
    'auto_install': False,
    'installable': True,
}
