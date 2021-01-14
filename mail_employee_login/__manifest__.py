# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "DAFA employee login email template",
    "version": "12.0.1.0.0",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "description": """
	Templates for Email, Eletters and SMS.
    """,
    "depends": [
        "hr",
        "auth_signup",
        "send_mail_nadim",
        ],
    "external_dependencies": [],
    "data": [
        "views/employee_view.xml",
        "data/employee_login_data.xml",
    ],
    "application": False,
    "installable": True,
    "auto_install": True,
}
