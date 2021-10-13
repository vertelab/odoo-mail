{
    "name": "AF Mass Mailing Snippets",
    "summary": "This version is used to customize the Odoo standard mail body widgets in accordance to 'Af' mail template.",
    "version": "12.0.0.0.7",
    "category": "Email Marketing",
    "description": """
    v12.0.0.1 AFC-2067  Added snippets in Mass mailing body.\n
    v12.0.0.2 AFC-2067 IMP  Added snippets in Mass mailing body.\n
    v12.0.0.3 AFC-2067 IMP  Added snippets in separate section of Mass mailing body.\n
    v12.0.0.4 AFC-2067 Fix  Fixed setting menu URL issue.\n
    v12.0.0.5 AFC-2067 Fix  Fixed Font and Background issue in Email.\n
    v12.0.0.6 AFC-1725 Added some more snippets in Mass mailing body\n
    v12.0.0.7 AFC-2725 Changed some style in snippets.\n
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
