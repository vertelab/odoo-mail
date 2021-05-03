# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Af ADKD Install modules",
    "version": "12.0.1.0.3",
    "author": "Swedish Public Employement Service",
    "license": "AGPL-3",
    "website": "https://arbetsformedlingen.se/",
    "category": "Tools",
    "depends": [
		"partner_mail_client",		# odoo-base This modules adds menus and tabs to display the contacts messages
		"mass_mailing",			# Odoo module for newsletters
		"mail_autoresponder",		# generic module to process automatic newsletters
		"mail_autoresponder_crm",	# CRM-addon to glue the module to CRM-specific views. (This depends on odoo-base/partner_daily_notes which depends onodoo-base/partner_view_360)
		"mail_browser_view",		# OCA module display the newsletter-email in the webbrowser
		"mail_improved_tracking_value",		# github.com/OCA/social This module extends the mail_tracking_value
		"mass_mailing_custom_unsubscribe",	# github.com/OCA/social  module Gives reasons for unsubscribe
		"mass_mailing_editor_af",		# odoo-mail This adds custom snippets to the mail-editor
		"mail_mass_mailing_gdrp_limitations",	# Module to hide personal-data in the Display Sample in MassMailing and Autoresponder-modules
		"mail_massmailing_statistics_af",	# odoo-mail This extends the statistics displayed in smart buttons to give percentages.


			],
    "application": False,
    "installable": True,
}

