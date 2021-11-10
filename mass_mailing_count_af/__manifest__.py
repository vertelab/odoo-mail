{
    "name": "Search Count Extension",
    "summary": "Sets config parameter to correct AF-Groups.",
    "version": "12.0.1.0.0",
    "category": "Email Marketing",
    "description": """
    1. 12.0.1.0.0 AFC-2879-Count-Extention - Add valid groups for AF
    """,
    "license": "AGPL-3",
    "maintainer": "Vertel AB",
    "author": "Vertel AB",
    "contributors": ["Nils Nyman-Waara",],
    "depends": ["mass_mailing_count",
                "mass_mailing"
    ],
    "data": ["data/groups.xml",
             "views/mass_mail_template_design.xml"
    ],
    "auto_install": False,
    "installable": True,
}
