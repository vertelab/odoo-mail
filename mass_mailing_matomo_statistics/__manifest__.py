{
    "name": "Mass mailing Matomo statistics AF",
    "summary": "This module will add snippet in Mass Mailing mail body to add Matomo image for email tracking.",
    "version": "12.0.0.1.1",
    "category": "Email Marketing",
    "description": """
    After installation of this module, Go to Setting >> Technical >> Parameter >> System Parameter. \n
    Update Matomo website URL and Website ID.\n
    1. Search key 'mass_mailing_matomo_statistics.website_url' for Website URL. Update value with Matomo website URL. \n 
    2. Search key 'mass_mailing_matomo_statistics.website_id' for Website ID. Update value with Matomo website ID.  \n\n
    
	 v12.0.0.1 AFC-2100c  Added snippet in Mass Mailing mail body to add Matomo image for email tracking.\n
	 v12.1.0.2 AFC-2984. Added a opt out all button on the mail.mass_mailing.contact form\n
	 v12.1.0.3 AFC-3010. Fixade opt out bug in the core module\n
     v12.0.0.4 AFC-2865 Added bouncing categories and a tree view to show them. There is a button when looking at bounces on a mass_mailing that will show the categories\n
     v12.0.1.0 AFC-3207 hide opt out all button for ADKD guest group\n
     v12.0.1.1 AFC-3074 Add external ID's.\n
    """,
    "license": "AGPL-3",
    "maintainer": "Vertel AB",
    "author": "Vertel AB",
    "contributors": ["Vertel AB"],
    "depends": [
        "mass_mailing", "af_security",
    ],
    "data": [
        'views/mass_mailing_views.xml',
        'views/snippets.xml',
        'data/ir.config_parameter.csv',
        'views/mailing_contact_tree_view.xml',
        'security/ir.model.access.csv'
    ],
    "auto_install": False,
    "installable": True,
}
