{
    "name": "Mass mailing statistics AF",
    "summary": "This module will show number for Email tracking events in Mass Mailing.",
    "version": "12.0.1.1.1",
    "category": "Email Marketing",
    "description": """
	 v12.0.0.1 AFC-2100  Added numbers for email tracking events in Mass mailing kanban and form view.\n
	 v12.1.0.0 AFC-2867  Added fields in mass mailing list view.\n
	 v12.1.0.1 AFC-3042  Fixed the total click calulation
	 v12.1.0.2 AFC-2943 Added clicks ratio to the report. Added to that we calulate the total number of clicks, so every
	 time a link has been pressed in a mail, and added that to the report.
	 v12.1.0.3 AFC-3125 Moved link tracker code to mass_mailing_statistics_af module.
	 v12.1.0.4 AFC-3474 Translated total clicks to totala klick.
     v12.1.0.5 AFC-3471 Cleaned up calculations.
     v12.1.0.6 AFC-3469 Translate fields to CTR 
     v12.1.0.7 AFC-3361 Add percentage sign to entries in tree view
     v12.1.0.8 AFC-3502 Change translation to field
<<<<<<< HEAD
     v12.1.0.9 AFC-3470 Hide replied view and changed filed in the kanban view.
     v12.1.1.0 AFC-3473 Calculate CTOR and add field to views
     v12.1.1.1 AFC-3506 Fixed calculation of CTR.
     v12.1.1.0 AFC-3473 Calculate CTOR and add field to views
    """,
    "license": "AGPL-3",
    "maintainer": "Vertel AB",
    "author": "Vertel AB",
    "contributors": ["Vertel AB"],
    "depends": [
        "mass_mailing",
        "link_tracker",
        
    ],
    "data": [
        'views/mass_mailing_views.xml',
        'views/mail_statistics_report_view.xml',
        'views/link_tracker.xml',
        'security/ir.model.access.csv',
    ],
    "qweb": [
        'static/src/xml/base.xml',
    ],
    "auto_install": False,
    "installable": True,
}
