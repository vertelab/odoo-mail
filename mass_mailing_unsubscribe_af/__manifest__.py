{
    "name": "Mass mailing unsubscribe AF",
    "summary": "Update layout of unsubscribe page.",
    "version": "12.0.1.6.6",
    "category": "Email Marketing",
    "description": """
	 v12.0.0.0.1 AFC-2173 Update layout of Unsubscribe Page.\n
	 v12.0.0.0.2 AFC-2173 Fixed bug with link.\n
	 v12.0.0.0.3 AFC-2341 Changed module name from mass_mailing_unsubscribe_nyhetsbrev_af to mass_mailing_unsubscribe_af.\n
	 v12.0.0.0.4 AFC-2410 Added Import wizard for Deregistration to Mass Mailing.\n
	 v12.0.0.0.5 AFC-2410 Allowed to import with text file. Added sample file to download.\n
     v12.0.1.0.0 AFC-2589 Bugfixes and cleanup of code, first stable version.\n
     v12.0.1.1.0 AFC-2721 Fixed view in the upload page.\n
     v12.0.1.1.1 AFC-2800 Bugfix for importing files in unsubscriptions.\n
     v12.0.1.2.0 AFC-2730 translated text.\n
     v12.0.1.2.1 AFC-2819 translated text.\n
     v12.0.1.2.2 AFC-2802 Small bugfix in import.\n
     v12.0.1.2.3 AFC-2851 Added proper date handling for opt out date in xls files.\n
     v12.0.1.2.4 AFC-2820 Add translation to menu items.\n
     v12.0.1.2.5 AFC-2912 Add security for mail.unsubscribe model.\n
     v12.0.1.3.0 AFC-2890 Add email to blacklist also.\n
     v12.0.1.3.0 AFC-3112 Buggfix, handle more dateformats.\n
     v12.0.1.3.1 AFC-3112 Buggfix, remove debuging raise.\n
     v12.0.1.3.2 AFC-3111 Buggfix, Do not access forbidden data.\n
     v12.0.1.4.0 AFC-3028 Created new access group ADKD manual guest and adjusted access right \n
     v12.0.1.5.0 AFC-3124 Changed from email to sökande id for matching unsubscribe contact \n
     v12.0.1.6.0 AFC-3305 Changed from email to sökande id for matching blacklist contact \n
     v12.0.1.6.1 AFC-3179 Change border color of textarea in unsubscription form \n
     v12.0.1.6.2 AFC-3203 Added some js to make a popup when clicking on unsubscription button \n
     v12.0.1.6.3 AFC-3136 Bugfix, can now access unsubscriber_id when creating unsubscription. \n
     v12.0.1.6.4 AFC-3199 Added label to textarea \n
     v12.0.1.6.5 AFC-3204 Change code to pass validation.\n
     v12.0.1.6.6 AFC-3363 Addes js to hide and show textarea based on radio button choice.\n
    """,
    "license": "AGPL-3",
    "maintainer": "Vertel AB",
    "author": "Vertel AB",
    "contributors": ["Vertel AB"],
    "depends": [
        "mass_mailing_custom_unsubscribe",'af_security'
    ],
    "external_dependencies": {"python": ['pytz', 'xlrd']},
    "data": [
        'security/ir.model.access.csv',
        'data/mail_unsubscription_reason.xml',
        'views/unsubsribe_views.xml',
        'views/assets.xml',
        'wizard/import_deregistration_views.xml'
    ],
    "auto_install": False,
    "installable": True,
}
