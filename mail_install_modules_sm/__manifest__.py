# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Af Säkra medddelanden Install modules",
    "version": "12.0.1.0.1",
    "author": "Swedish Public Employement Service",
	"contributor": "Swedish Public Employement Service, Vertel AB",
    "license": "AGPL-3",
    "website": "https://arbetsformedlingen.se/",
    "description": "This module is maintained here https://github.com/vertelab/odoo-mail/tree/Dev-12.0/mail_install_modules_sm",
    "category": "Tools",
    "depends": [
		"hr_employee_mail_client", # odoo-hr This module adds a tab with messages on the employee-form
		"partner_mail_client",     # odoo-base This module adds a tab with messages on the partner-form
			],
    "application": False,
    "installable": True,
}

