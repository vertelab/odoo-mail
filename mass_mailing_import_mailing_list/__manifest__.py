# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Import mailing list',
    'summary': "Import mailing list for mass mailing",
    'version': '12.0.1.0.1',
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'maintainer': 'Vertel AB',
    'description': """
        - 12.0.1.0.1  AFC-2117-2 New module for importing mailing list \n
    """,
    'website': 'http://www.vertel.se',
    'depends': ['mass_mailing'],
    'data': [
        'wizard/import_mailing_list_wizard.xml',
    ],
    'auto_install': False,
    'installable': True,
}
