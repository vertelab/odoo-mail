# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "DAFA Outplacement Templates",
    "version": "12.0.1.0.0",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "description": """
	Templates for Email, Eletters and SMS.
    """,
    "depends": [
        "auth_signup"],
    "external_dependencies": [],
    "data": [
        "reports/welcome_letter_report.xml",
        "data/auth_signup_custom_data.xml",
    ],
    "application": False,
    "installable": True,
    'auto_install': True,
}
