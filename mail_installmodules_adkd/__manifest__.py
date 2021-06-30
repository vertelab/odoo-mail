# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Af ADKD Install modules",
    "version": "12.0.1.0.4",
    "author": "Swedish Public Employement Service",
    "license": "AGPL-3",
    "website": "https://arbetsformedlingen.se/",
    "description": "This module is maintained here https://github.com/vertelab/odoo-mail/tree/Dev-12.0/mass_mailing_unsubscribe_af",
    "category": "Tools",
    "depends": [
   	        # "partner_mail_client",		# odoo-base This modules adds menus and tabs to display the contacts messages. Is replaced by mail_partner_messages
		"mass_mailing",			# Odoo module for newsletters
		"mail_autoresponder",		# generic module to process automatic newsletters
		"mail_autoresponder_crm",	# CRM-addon to glue the module to CRM-specific views. (This depends on odoo-base/partner_daily_notes which depends onodoo-base/partner_view_360)
		"mail_browser_view",		# OCA module display the newsletter-email in the webbrowser
		"mail_improved_tracking_value",		# github.com/OCA/social This module extends the mail_tracking_value
		"mass_mailing_custom_unsubscribe",	# github.com/OCA/social  module Gives reasons for unsubscribe
		"mass_mailing_editor_af",		# odoo-mail This adds custom snippets to the mail-editor
		"mass_mailing_gdpr_limitations",	# Module to hide personal-data in the Display Sample in MassMailing and Autoresponder-modules
		"mass_mailing_statistics_af",	# odoo-mail This extends the statistics displayed in smart buttons to give percentages.
	    	"mass_mailing_unsubscribe_af",		# Fixes layout of unsubscribe-page https://github.com/vertelab/odoo-mail/tree/Dev-12.0/mass_mailing_unsubscribe_af
		"mail_partner_messages",		# Adds a tab with messages to the contact and jobseeker view. https://github.com/vertelab/odoo-mail/tree/Dev-12.0/mail_partner_messages


			],
    "application": False,
    "installable": True,
}

