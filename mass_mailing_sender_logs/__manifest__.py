{
    "name": "AF Mass Mailing Sender Logs",
    "summary": "This module adds logger in Email Marketing >> Mailing.",
    "version": "12.0.1.0.3",
    "category": "Email Marketing",
    "description": """
	 v12.0.0.1 AFC-2185 Added logger in Email Marketing >> Mailing.\n
	 v12.0.1.0.2 AFC-2185 Updated code for Logs.\n
	 v12.0.1.0.3 AFC-2394 Changed technical name\n
    """,
    "license": "AGPL-3",
    "maintainer": "Vertel AB",
    "author": "Vertel AB",
    "contributors": ["Vertel AB"],
    "depends": [
        "mass_mailing"
    ],
    "data": [
        'views/mass_mailing_views.xml'
    ],
    "auto_install": False,
    "installable": True,
}
