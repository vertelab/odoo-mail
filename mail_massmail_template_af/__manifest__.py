{
    "name": "AF Mass Mailing Template",
    "summary": "Adds a Mass Mailing Template Design",
    "version": "12.0.1.1.4",
    "category": "Email Marketing",
	"description": """
	 v12.0.0.1 AFC-86  Add Mass mailing template for AF newsletters.\n
	 v12.0.0.2  This version fixes bug in the template and makes the AF-template be visible beside the other templates.\n
	 v12.0.1.1.0 Change name\n
	 v12.0.1.1.3 Added link to view in browser\n
	 v12.0.1.1.4 Moved back to vertel odoo-mail\n
	 
    """,
    "license": "AGPL-3",
    "maintainer": "Swedish Public Employement Service",
	"author": "Vertel AB",
	"contributors": ['Swedish Public Employement Service', 'Vertel AB', 'Harhu Technologies Pvt. Ltd.'],
    "depends": [
        "mass_mailing"
    ],
    'data': [
        "data/mail_template.xml",
    ],
    'installable': True,
}
