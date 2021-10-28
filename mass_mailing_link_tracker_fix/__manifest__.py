{
    "name": "Mass mailing Link Tracker Fix",
    "summary": "This module will show number for Email tracking events in Mass Mailing.",
    "version": "12.0.0.1.0",
    "category": "Email Marketing",
    "description": """
	 v12.0.1.0 AFC-2864  Added a Controller that will redirect from odoo to another link, so that we can measure unique and total klicks and still send the user to the 
	 correct url.\n

    """,
    "license": "AGPL-3",
    "maintainer": "Vertel AB",
    "author": "Vertel AB",
    "contributors": ["Vertel AB"],
    'depends': ['base', 'link_tracker'],
    'data': ['views/link_tracker.xml'],
    "qweb": [
        'static/src/xml/base.xml',
    ],
    "auto_install": False,
    "installable": True,
}

