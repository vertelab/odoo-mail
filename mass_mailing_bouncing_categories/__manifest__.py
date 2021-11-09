{
    "name": "Mass mailing Bounce Categories AF",
    "summary": "This module will show bounce categories with code/diagnostic message.",
    "version": "12.0.0.0.0",
    "category": "Email Marketing",
    "description": """
	 v12.0.0.0 AFC-2865 Added bouncing categories and a tree view to show them. There is a button viewing bounces on a mass_mailing that will show the categories\n

    """,
    "license": "AGPL-3",
    "maintainer": "Vertel AB",
    "author": "Vertel AB",
    "contributors": ["Vertel AB"],
    "depends": [
        "mass_mailing"
    ],
    "data": [
        'views/mailing_contact_tree_view.xml',
        'security/ir.model.access.csv'
    ],
    "qweb": [
        'static/src/xml/base.xml',
    ],
    "auto_install": False,
    "installable": True,
}

