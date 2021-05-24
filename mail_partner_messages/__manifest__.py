{
    "name": "Mail Partner Messages",
    "summary": "Mail Client Contact",
    "version": "12.0.1.0.4",
    "category": "Messaging",
	"description": """
	 v12.0.0.1 AFC-1313 Mail Client Odoo Messaging.
	 v12.0.0.2 AFC-2322 Added new tab inside Contact & Jobseeker and new menu 'Messages' for Mass mailing messages for Newsletter >> Manual user group.
	 v12.0.1.0.3 Fixed numbering and Name in manifest
	 v12.0.1.0.4 AFC-2322 Added Email button on Message to redirect Email, Added statistics on Messages, Set 'Keep Archive' default true and required.
	 
	     """,
    "license": "AGPL-3",
    "author": "Vertel AB",
    "depends": [
        "mass_mailing", "contacts", "sale_management", "crm", "partner_view_360"
    ],
    'data': [
        "security/ir.model.access.csv",
        "views/mass_mailing_message_views.xml",
    ],
    'installable': True,
}
