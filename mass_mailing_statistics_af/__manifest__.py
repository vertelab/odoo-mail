{
    "name": "Mass mailing statistics AF",
    "summary": "This module will show number for Email tracking events in Mass Mailing.",
    "version": "12.0.2.1.2",
    "category": "Email Marketing",
    "description": """
     v12.0.0.1 AFC-2100  Added numbers for email tracking events in Mass mailing kanban and form view.\n
     v12.1.0.0 AFC-2867  Added fields in mass mailing list view.\n
     v12.1.0.1 AFC-3042  Fixed the total click calculation
     v12.1.0.2 AFC-2943 Added clicks ratio to the report. Added to that we calculate the total number of clicks, so every
     time a link has been pressed in a mail, and added that to the report.
     v12.1.0.3 AFC-3125 Moved link tracker code to mass_mailing_statistics_af module.
     v12.1.0.4 AFC-3474 Translated total clicks to totala klick.
     v12.1.0.5 AFC-3471 Cleaned up calculations.
     v12.1.0.6 AFC-3469 Translate fields to CTR 
     v12.1.0.7 AFC-3361 Add percentage sign to entries in tree view
     v12.1.0.8 AFC-3502 Change translation to field
     v12.1.0.9 AFC-3470 Hide replied view and changed filed in the kanban view.
     v12.1.1.0 AFC-3473 Calculate CTOR and add field to views
     v12.1.1.1 AFC-3506 Fixed calculation of CTR.
     v12.1.1.2 AFC-3477 Redid the calculation for opened_ratio field and added it in some views.
     v12.1.1.3 AFC-3507 separated the columns that displayed very close to each other, repleaced delivered field with recived field in the list table.
     v12.1.1.4 AFC-3521 Add translation
     v12.1.1.5 AFC-3471 Fixing CTR calculations.
     v12.1.1.6 AFC-3471 Bugfix of CTR and CTOR calculations.
     v12.1.1.7 AFC-3528 Add translation
     v12.1.2.0 AFC-3530 Add unsubscription button and changed order of the buttons
     v12.2.0.0 AFC-3495 Changed view in kanban box and action
     v12.2.1.0 AFC-3540 Added basic unit tests.
     v12.2.1.1 AFC-3548 Changed name of the field
     v12.2.1.2 AFC-3547 updated how the field looks like
    """,
    "license": "AGPL-3",
    "maintainer": "Vertel AB",
    "author": "Vertel AB",
    "contributors": ["Vertel AB"],
    "depends": [
        "mass_mailing",
        "link_tracker",
        "mass_mailing_unsubscribe_af"
        
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
