{
    "name": "AF Mass Mailing gdpr limitations",
    "summary": "This module limits the disclosure of personal data in the mass-mailing module",
    "version": "12.0.0.0.1",
    "category": "Email Marketing",
    "description": """
	 12.0.0.0.1  AFC-2167 Updated list view of contacts from Email marketing smart buttons.
    """,
    "license": "AGPL-3",
    "maintainer": "Vertel AB",
    "author": "Vertel AB",
    "contributors": ["Vertel AB"],
    "depends": [
        "mass_mailing", "partner_view_360"
    ],
    "data": [
        "views/res_partner_view.xml"
    ],
    "auto_install": False,
    "installable": True,
}

