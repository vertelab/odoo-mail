{
    "name": "Mass Mailing Server Actions",
    "summary": "Adds server actions to Massmailing module.",
    "version": "12.0.1.0.0",
    "category": "Email Marketing",
    "description": """
    1. 12.0.1.0.0 AFC-3015 - Add run mass mailning queue manually. 
    """,
    "license": "AGPL-3",
    "maintainer": "Vertel AB",
    "author": "Vertel AB",
    "contributors": ["Nils Nyman-Waara",],
    "depends": ["mass_mailing"
                ],
    "data": ["data/server_actions.xml",
             ],
    "auto_install": False,
    "installable": True,
}