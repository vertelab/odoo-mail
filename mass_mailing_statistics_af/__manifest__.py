{
    "name": "AF Mass mailing statistics",
    "summary": "This module will show number for Email tracking events in Mass Mailing.",
    "version": "12.0.0.0.2",
    "category": "Email Marketing",
    "description": """
	 v12.0.0.1 AFC-2100  Added numbers for email tracking events in Mass mailing kanban and form view.\n
	 v12.0.0.2 AFC-2394 Changed display and technical name\n
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
    ],
    "qweb": [
        'static/src/xml/base.xml',
    ],
    "auto_install": False,
    "installable": True,
}

