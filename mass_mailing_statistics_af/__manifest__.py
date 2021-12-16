{
    "name": "Mass mailing statistics AF",
    "summary": "This module will show number for Email tracking events in Mass Mailing.",
    "version": "12.0.1.0.2",
    "category": "Email Marketing",
    "description": """
	 v12.0.0.1 AFC-2100  Added numbers for email tracking events in Mass mailing kanban and form view.\n
	 v12.1.0.0 AFC-2867  Added fields in mass mailing list view.\n
	 v12.1.0.1 AFC-3042  Fixed the total click calulation
	 v12.1.0.2 AFC-2943 Added clicks ratio to the report. Added to that we calulate the total number of clicks, so every
	 time a link has been pressed in a mail, and added that to the report.
    """,
    "license": "AGPL-3",
    "maintainer": "Vertel AB",
    "author": "Vertel AB",
    "contributors": ["Vertel AB"],
    "depends": [
        "mass_mailing",
        'mass_mailing_sender_logs',#until the link tracker logic is moved from mass_mailing_sender_logs, then this module needs to depend on it.
        
    ],
    "data": [
        'views/mass_mailing_views.xml',
        'views/mail_statistics_report_view.xml',
    ],
    "qweb": [
        'static/src/xml/base.xml',
    ],
    "auto_install": False,
    "installable": True,
}

