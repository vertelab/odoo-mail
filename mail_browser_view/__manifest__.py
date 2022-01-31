# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Mail Browser View",
    "summary": "Add 'View this email in browser' feature",
    "version": "12.0.1.0.3",
    "category": "Social Network",
    "website": "https://github.com/OCA/social",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "description": """
        12.0.1.0.1  Fixed bug, wrong html code \n
        12.0.1.0.2  Generate proper unsubscribe url into html body \n
        12.0.1.0.3  Add title tag into html head \n
    """,
    "application": False,
    "installable": True,
    "depends": [
        "mail",
    ],
    "data": [
        "data/ir_config.xml",
    ],
    "demo": [
        "demo/mail.xml",
    ]
}
