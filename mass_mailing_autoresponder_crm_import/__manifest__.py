# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Mail Autoresponder CRM Import',
    'summary': "Adds an import message log",
    'version': '12.0.1.0.1',
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'maintainer': 'Vertel AB',
    'description': """
        - 12.0.1.0.1  AFC-2117 Added import wizard for knime exports\n
    """,
    'website': 'http://www.vertel.se',
    'depends': ['mass_mailing_autoresponder_crm'],
    'data': [
        'wizard/import_knime_export_wizard.xml',
    ],
    'auto_install': False,
    'installable': True,
}
