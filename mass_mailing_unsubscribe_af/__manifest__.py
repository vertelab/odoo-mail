{
    "name": "Mass mailing unsubscribe AF",
    "summary": "Update layout of unsubscribe page.",
    "version": "12.0.0.0.3",
    "category": "Email Marketing",
    "description": """
	 v12.0.0.1 AFC-2173  Update layout of Unsubscribe Page.\n
	 v12.0.0.2 AFC-2173 Fixed bug with link.\n
	 v12.0.0.3 AFC-2341 Changed module name from mass_mailing_unsubscribe_nyhetsbrev_af to mass_mailing_unsubscribe_af.\n
    """,
    "license": "AGPL-3",
    "maintainer": "Vertel AB",
    "author": "Vertel AB",
    "contributors": ["Vertel AB"],
    "depends": [
        "mass_mailing_custom_unsubscribe"
    ],
    "data": [
        'data/mail_unsubscription_reason.xml',
        'views/unsubsribe_views.xml',
        'views/assets.xml'
    ],
    "auto_install": False,
    "installable": True,
}

