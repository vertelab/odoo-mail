# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "DAFA Outplacement Templates",
    "version": "12.0.2.0.1",
    "author": "Vertel AB",
    "license": "AGPL-3",
    "website": "https://vertel.se/",
    "category": "Tools",
    "description": "Templates for Email, Eletters and SMS.",
    "depends": [
        "hr",
        "outplacement",
        ],
    "external_dependencies": [],
    "data": [
        "views/outplacement_view.xml",
        "reports/assigned_coach_report.xml",
        "data/employee_login_data.xml",
        #"data/assigned_coach_data.xml",
        "data/assigned_coach_data_edit.xml",
        
    ],
    "application": False,
    "installable": True,
}
