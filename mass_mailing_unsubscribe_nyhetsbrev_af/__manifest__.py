{
    "name": "Mass mailing unsubscribe nyhetsbrev AF",
    "summary": "Update layout of unsubscribe page.",
    "version": "12.0.0.0.1",
    "category": "Email Marketing",
    "description": """
	 v12.0.0.1 AFC-2173  Update layout of Unsubscribe Page.\n
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
    ],
    "auto_install": False,
    "installable": True,
}
