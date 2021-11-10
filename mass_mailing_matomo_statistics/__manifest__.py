{
    "name": "Mass mailing Matomo statistics AF",
    "summary": "This module will add snippet in Mass Mailing mail body to add Matomo image for email tracking.",
    "version": "12.0.0.0.2",
    "category": "Email Marketing",
    "description": """
    After installation of this module, Go to Setting >> Technical >> Parameter >> System Parameter. \n
    Update Matomo website URL and Website ID.\n
    1. Search key 'mass_mailing_matomo_statistics.website_url' for Website URL. Update value with Matomo website URL. \n 
    2. Search key 'mass_mailing_matomo_statistics.website_id' for Website ID. Update value with Matomo website ID.  \n\n
    
	 v12.0.0.1 AFC-2100c  Added snippet in Mass Mailing mail body to add Matomo image for email tracking.\n
	 v12.0.0.2 AFC-2865 Added bouncing categories and a tree view to show them. There is a button when looking at bounces on a mass_mailing that will show the categories\n
    """,
    "license": "AGPL-3",
    "maintainer": "Vertel AB",
    "author": "Vertel AB",
    "contributors": ["Vertel AB"],
    "depends": [
        "mass_mailing",
    ],
    "data": [
        'views/snippets.xml',
        'data/ir.config_parameter.csv',
        'views/mailing_contact_tree_view.xml',
        'security/ir.model.access.csv'
    ],
    "auto_install": False,
    "installable": True,
}

