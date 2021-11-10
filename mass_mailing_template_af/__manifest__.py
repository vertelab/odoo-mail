{
    "name": "AF Mass Mailing Template",
    "summary": "Adds a Mass Mailing Template Design",
    "version": "12.0.1.3.2",
    "category": "Email Marketing",
    "description": """
    v12.0.0.1 AFC-86  Add Mass mailing template for AF newsletters.\n
    v12.0.0.2  This version fixes bug in the template and makes the AF-template be visible beside the other templates.\n
    v12.0.1.1.0 Change name\n
    v12.0.1.1.3 Added link to view in browser\n
    v12.0.1.1.4 Moved back to vertel odoo-mail\n
    v12.0.1.1.5 AFC-1725 Added two more sample templates and hide Odoo standard templates.\n
    v12.0.1.1.6 AFC-1725 Added dynamic links and updated some styles on sample templates.\n
    v12.0.1.1.7 Fixed typos in templates.\n
    v12.0.1.1.8 AFC-2725 Changed some style in both templates.\n
    v12.0.1.2.0 AFC-2826 Disabled resizing snippets in editor.\n
    v12.0.1.2.1 AFC-2977 Changed style in templates, moved background color for mail client to render correctly.\n
    v12.0.1.3.0 AFC-2829 Added empty snippets above and below all snippets for moving vertically.\n
    v12.0.1.3.1 AFC-2830 Changed background color to skip inherit color when snippet moving.\n
    v12.0.1.3.2 AFC-3009 It is unable now to come across and drag out the content of snippets.\n
    """,
    "license": "AGPL-3",
    "maintainer": "Swedish Public Employement Service",
    "author": "Vertel AB",
    "contributors": ['Swedish Public Employement Service', 'Vertel AB', 'Harhu Technologies Pvt. Ltd.'],
    "depends": [
        "mass_mailing", "mail_browser_view"
    ],
    'data': [
        "data/mail_template.xml",
        "views/assets.xml",
    ],
    'installable': True,
}
