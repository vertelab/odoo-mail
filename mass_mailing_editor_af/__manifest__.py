{
    "name": "AF Mass Mailing Snippets",
    "summary": "This version is used to customize the Odoo standard mail body widgets in accordance to 'Af' mail template.",
    "version": "12.0.0.0.2",
    "category": "Email Marketing",
    "description": """
	 v12.0.0.1 AFC-2067  Added snippets in Mass mailing body.\n
	 v12.0.0.2 AFC-2067 IMP  Added snippets in Mass mailing body.\n
    """,
    "license": "AGPL-3",
    "maintainer": "Vertel AB",
    "author": "Vertel AB",
    "contributors": ["Vertel AB"],
    "depends": [
        "mass_mailing"
    ],
    "data": [
        'views/snippets_themes.xml',
        'views/assets.xml'
    ],
    "auto_install": False,
    "installable": True,
}

