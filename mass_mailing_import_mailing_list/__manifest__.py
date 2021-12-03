# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Import mailing list',
    'summary': "Import mailing list for mass mailing",
    'version': '12.0.1.0.4',
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'maintainer': 'Vertel AB',
    'description': """
        - 12.0.1.0.0  AFC-2968 New module for importing mailing list \n
        - 12.0.1.0.1  AFC-2874 Some error handling \n
        - 12.0.1.0.2  AFC-3135 Bugfix, able to read .txt files again \n
        - 12.0.1.0.3  AFC-3135-2 Bugfix, changed to right index in filename split\n
        - 12.0.1.0.4  AFC-3170 Hide import list menu for ADKD guest group\n
    """,
    'website': 'http://www.vertel.se',
    'depends': ['mass_mailing', 'mass_mailing_unsubscribe_af'],
    'data': [
        'wizard/import_mailing_list_wizard.xml',
    ],
    'auto_install': False,
    'installable': True,
}
