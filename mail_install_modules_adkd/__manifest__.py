# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Af ADKD Install modules",
    "version": "12.0.1.0.5",
    "author": "Swedish Public Employement Service",
    "license": "AGPL-3",
    "website": "https://arbetsformedlingen.se/",
    "description": """
    This module is maintained here https://github.com/vertelab/odoo-mail/blob/Dev-12.0/mail_install_modules_adkd
    v12.0.1.0.4 AFC-2658 Added ',' between depends modules
    v12.0.1.0.5 AFC-2658 Corrected wrong module name
    """,
    "category": "Tools",
    "depends": [
        "fetchmail",                        # odoo-core-module. Needed but not used by us.
        "hr_employee_mail_client",          # odoo-hr This adds a tab on the Employee form for messages sent to and from that employee.
        # "mail_bot",                       # odoo-core-module. Needed but not used by us.
        "mail_browser_view",                # https://github.com/OCA/social A module for reading newsletters through a webpage.
        "mail_improved_tracking_value",     # https://github.com/OCA/social A module improved tracking. This is optional now.
        "mass_mailing",                     # Odoo module for newsletters
        "mass_mailing_autoresponder",       # generic module to process automatic newsletters
        "mass_mailing_autoresponder_crm",   # CRM-addon to glue the module to CRM-specific views. (This depends on odoo-base/partner_daily_notes which depends onodoo-base/partner_view_360)
        "mail_browser_view",                # github.com/OCA/social A module display the newsletter-email in the webbrowser
        "mail_improved_tracking_value",     # github.com/OCA/social This module extends the mail_tracking_value
        "mass_mailing_custom_unsubscribe",  # github.com/OCA/social  module Gives reasons for unsubscribe
        "mass_mailing_editor_af",           # odoo-mail This adds custom snippets to the mail-editor
        "mass_mailing_gdrp_limitations",    # odoo-mail A Module to hide personal-data in the Display Sample in MassMailing and Autoresponder-modules
        "mass_mailing_matomo_statistics",   # odoo-mail Adds a tracking image as a Snippet in the mail-templates.
        "mass_mailing_statistics_af",       # odoo-mail This extends the statistics displayed in smart buttons to give percentages.
        "mass_mailing_unsubscribe_af",      # Odoo-mail Fixes layout of unsubscribe-page
        "mail_partner_messages",            # Odoo-mail Adds a tab with messages to the contact and jobseeker view.
        "mass_mailing_template_af",         # odoo-mail This adds new sample mass mailing templates and hide odoo standard's mass mailing templates.
        "mass_mailing_editor_af",           # odoo-mail This adds new snippets for mass mailing templates.
        "partner_mail_client",              # odoo-base This adds a tab on the Employee form for messages sent to and from that partner.
        "mass_mailing_count_af",            # Extends the standard search_count widget with Sudo search.
        "mass_mailing_multi_per_address_af", # Extends the standard mass_mailing to fix the bug when contact share the same email address.
        # "snailmail",                      # Odoo standard-module that is not used in our implementation.
    ],
    "application": False,
    "installable": True,
}

