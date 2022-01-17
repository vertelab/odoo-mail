{
    "name": "AF Mass Mailing Snippets",
    "summary": "This version is used to customize the Odoo standard mail body widgets in accordance to 'Af' mail template.",
    "version": "12.0.0.2.1",
    "category": "Email Marketing",
    "description": """
    v12.0.0.0.1 AFC-2067  Added snippets in Mass mailing body.\n
    v12.0.0.0.2 AFC-2067 IMP  Added snippets in Mass mailing body.\n
    v12.0.0.0.3 AFC-2067 IMP  Added snippets in separate section of Mass mailing body.\n
    v12.0.0.0.4 AFC-2067 Fix  Fixed setting menu URL issue.\n
    v12.0.0.0.5 AFC-2067 Fix  Fixed Font and Background issue in Email.\n
    v12.0.0.0.6 AFC-1725 Added some more snippets in Mass mailing body\n
    v12.0.0.0.7 AFC-2725 Changed some style in snippets.\n
    v12.0.0.1.0 AFC-2829 Added empty snippets above and below all templates for drag and drop.\n
    V12.0.0.1.1 AFC-2830 Changed background color to skip inherit color when snippet moving.\n
    V12.0.0.1.2 AFC-3009 It is unable now to come across and drag out the content of snippets.\n
    V12.0.0.1.3 AFC-3066 Fixed a minor bug for background color (till guiden) and (till tipset) snippets.\n
    V12.0.0.2.0 AFC-3208 Added field for internal name of massmailings.\n
    v12.0.0.2.1 AFC-3182 Change text color on link to ensure level of contrast.\n
    """,
    "license": "AGPL-3",
    "maintainer": "Vertel AB",
    "author": "Vertel AB",
    "contributors": ["Vertel AB"],
    "depends": [
        "mass_mailing"
    ],
    "data": [
        'views/mass_mailing_views.xml',
        'views/snippets_themes.xml',
        'views/assets.xml'
    ],
    "auto_install": False,
    "installable": True,
}
