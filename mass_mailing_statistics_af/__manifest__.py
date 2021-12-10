{
    "name": "Mass mailing statistics AF",
    "summary": "This module will show number for Email tracking events in Mass Mailing.",
    "version": "12.0.1.0.1",
    "category": "Email Marketing",
    "description": """
    v12.0.0.1 AFC-2100  Added numbers for email tracking events in Mass mailing kanban and form view.\n
    v12.1.0.0 AFC-2867  Added fields in mass mailing list view.\n
    v12.1.0.1 AFC-3042  Fixed the total click calulation
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
