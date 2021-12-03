# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from lxml import etree


class EventEmailAudit(models.Model):

    _name = 'event.email.audit'

    _description = 'Autoreponder Email Audit'

    user_id = fields.Many2one("res.users", "Sent through")
    partner_id = fields.Many2one("res.partner")
    email = fields.Char(related="partner_id.email", string="Email", store=True)
    sent_time = fields.Datetime("Sent Time")
    response = fields.Text("Response")
    event_id = fields.Many2one("partner.event", "Event")
    event_line_id = fields.Many2one("partner.event.email.schedule", "Event Line")


class MailMassMailing(models.Model):
    _inherit = 'mail.mass_mailing'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        result = super(MailMassMailing, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)

        # Disabling the import button for users who are not in import group
        if view_type == 'tree':
            doc = etree.XML(result['arch'])
            if not self.env.user.has_group('af_security.af_newsletter_manual'):
                # When the user is not part of the import group
                for node in doc.xpath("//tree"):
                    # Set the import to false
                    node.set('import', 'false'),
                    node.set('create', 'false')
            result['arch'] = etree.tostring(doc)
        elif view_type == 'kanban':
            doc = etree.XML(result['arch'])
            if not self.env.user.has_group('af_security.af_newsletter_manual'):
                # When the user is not part of the import group
                for node in doc.xpath("//kanban"):
                    # Set the import to false
                    node.set('import', 'false'),
                    node.set('create', 'false')
            result['arch'] = etree.tostring(doc)
        elif view_type == 'form':
            doc = etree.XML(result['arch'])
            if not self.env.user.has_group('af_security.af_newsletter_manual'):
                # When the user is not part of the import group
                for node in doc.xpath("//form"):
                    # Set the import to false
                    node.set('edit', 'false'),
                    node.set('create', 'false')
            result['arch'] = etree.tostring(doc)

        return result


class MassMailingList(models.Model):
    _inherit = 'mail.mass_mailing.list'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        result = super(MassMailingList, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)

        # Disabling the import button for users who are not in import group
        if view_type == 'tree':
            doc = etree.XML(result['arch'])
            if not self.env.user.has_group('af_security.af_newsletter_manual'):
                # When the user is not part of the import group
                for node in doc.xpath("//tree"):
                    # Set the import to false
                    node.set('import', 'false'),
                    node.set('create', 'false')
            result['arch'] = etree.tostring(doc)
        elif view_type == 'kanban':
            doc = etree.XML(result['arch'])
            if not self.env.user.has_group('af_security.af_newsletter_manual'):
                # When the user is not part of the import group
                for node in doc.xpath("//kanban"):
                    # Set the import to false
                    node.set('import', 'false'),
                    node.set('create', 'false')
            result['arch'] = etree.tostring(doc)

        return result


class MassMailingContact(models.Model):
    _inherit = 'mail.mass_mailing.contact'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        result = super(MassMailingContact, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)

        # Disabling the import button for users who are not in import group
        if view_type == 'tree':
            doc = etree.XML(result['arch'])
            if not self.env.user.has_group('af_security.af_newsletter_manual'):
                # When the user is not part of the import group
                for node in doc.xpath("//tree"):
                    # Set the import to false
                    node.set('import', 'false'),
                    node.set('create', 'false')
            result['arch'] = etree.tostring(doc)
        elif view_type == 'kanban':
            doc = etree.XML(result['arch'])
            if not self.env.user.has_group('af_security.af_newsletter_manual'):
                # When the user is not part of the import group
                for node in doc.xpath("//kanban"):
                    # Set the import to false
                    node.set('import', 'false'),
                    node.set('create', 'false')
            result['arch'] = etree.tostring(doc)

        return result


class MailBlackList(models.Model):
    _inherit = 'mail.blacklist'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        result = super(MailBlackList, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)

        # Disabling the import button for users who are not in import group
        if view_type == 'tree':
            doc = etree.XML(result['arch'])
            if not self.env.user.has_group('af_security.af_newsletter_manual'):
                # When the user is not part of the import group
                for node in doc.xpath("//tree"):
                    # Set the import to false
                    node.set('import', 'false'),
                    node.set('create', 'false')
            result['arch'] = etree.tostring(doc)
        elif view_type == 'form':
            doc = etree.XML(result['arch'])
            if not self.env.user.has_group('af_security.af_newsletter_manual'):
                # When the user is not part of the import group
                for node in doc.xpath("//form"):
                    # Set the import to false
                    node.set('edit', 'false'),
                    node.set('create', 'false')
            result['arch'] = etree.tostring(doc)

        return result


class MailUnsubscriptionReason(models.Model):
    _inherit = "mail.unsubscription.reason"

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        result = super(MailUnsubscriptionReason, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)

        # Disabling the import button for users who are not in import group
        if view_type == 'tree':
            doc = etree.XML(result['arch'])
            if not self.env.user.has_group('af_security.af_newsletter_manual'):
                # When the user is not part of the import group
                for node in doc.xpath("//tree"):
                    # Set the import to false
                    node.set('import', 'false'),
                    node.set('create', 'false')
            result['arch'] = etree.tostring(doc)
        elif view_type == 'form':
            doc = etree.XML(result['arch'])
            if not self.env.user.has_group('af_security.af_newsletter_manual'):
                # When the user is not part of the import group
                for node in doc.xpath("//form"):
                    # Set the import to false
                    node.set('edit', 'false'),
                    node.set('create', 'false')
            result['arch'] = etree.tostring(doc)

        return result


