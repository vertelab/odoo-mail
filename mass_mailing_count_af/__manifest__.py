{
    "name": "Search Count Extension",
    "summary": "Sets config parameter to correct AF-Groups.",
    "version": "12.0.1.1.2",
    "category": "Email Marketing",
    "description": """
    v 12.0.1.1.1 - AFC-3158 - Deleted repeated group name.\n 
    v 12.0.1.1.2 - AFC-3259 - Adjust access right for guest group.\n 
    """,
    "license": "AGPL-3",
    "maintainer": "Vertel AB",
    "author": "Vertel AB",
    "contributors": ["Nils Nyman-Waara",
                     "Sinan Özbek",
                     ],
    "depends": ["mass_mailing_count",
                "mass_mailing"
    ],
    "data": ["data/groups.xml",
             "views/mass_mail_template_design.xml"
    ],
    "auto_install": False,
    "installable": True,
}
