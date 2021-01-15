# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "DAFA Outplacement Templates",
    "version": "12.0.2.0.0",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "description": """
	Templates for Email, Eletters and SMS.
    """,
    "depends": [
        "hr",
        "outplacement",
        "auth_signup",
        "send_mail_nadim",
        ],
    "external_dependencies": [],
    "data": [
        "views/employee_view.xml",
        "reports/assigned_coach_report.xml",
        "data/assigned_coach_data.xml",
        "data/employee_login_data.xml",
    ],
    "application": False,
    "installable": True,
    "auto_install": True,
}
