# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class LinkTracker(models.Model):
    _inherit = 'link.tracker'
    user_clicks_per_link = fields.One2many('link.tracker.click.user.clicks.per.link', 'link_tracker_id', string='Non unique clicks')
    count_user_clicks_per_link = fields.Integer(string='Number of Clicks', compute='_compute_count_user_clicks_per_link', store=True)
    count = fields.Integer(string='Number of Unique Clicks', compute='_compute_count', store=True)

    @api.one
    @api.depends('user_clicks_per_link')
    def _compute_count_user_clicks_per_link(self):
        self.count_user_clicks_per_link = len(self.user_clicks_per_link)

    @api.multi
    def action_individual_unique_clicks_tree_view(self):
        tree_view_id = self.env.ref('mass_mailing_sender_logs.view_link_tracker_unique_click_tree').id
        return {
            'name': 'Individual Clicks',
            'type': 'ir.actions.act_window',
            'res_model': 'link.tracker.click',
            'view_type': 'form',
            'view_mode': 'tree',
            'domain': [('id', 'in', self.link_click_ids.mapped('id'))],
            'view_id': tree_view_id,
            'res_id': False,
            'context': False,
            'target': 'new',
        }

    @api.multi
    def action_individual_clicks_tree_view(self):
        tree_view_id = self.env.ref('mass_mailing_sender_logs.view_link_tracker_click_tree').id
        return {
            'name': 'Individual Clicks',
            'type': 'ir.actions.act_window',
            'res_model': 'link.tracker.click.user.clicks.per.link',
            'view_type': 'form',
            'view_mode': 'tree',
            'domain': [('id', 'in', self.user_clicks_per_link.mapped('id'))],
            'view_id': tree_view_id,
            'res_id': False,
            'context': False,
            'target': 'new',
        }


# Used to track each time a a mail_receiver clicks the same link.
# In order to keep track of the date of each click we create a new one each time a user clicks a link.
class LinkTrackerClickUserClicks(models.Model):
    _name = "link.tracker.click.user.clicks.per.link"
    click_date = fields.Datetime(string='Create Date')
    ip = fields.Char(string='Internet Protocol')
    country_id = fields.Many2one('res.country', 'Country')
    customer_id = fields.Char(string="Kundnummer")
    link_tracker_id = fields.Many2one('link.tracker', 'Link Tracker', required=True, ondelete='cascade')
    mail_stat_id = fields.Many2one('mail.mail.statistics', string='Mail Statistics')

class LinkTrackerClick(models.Model):
    _inherit = "link.tracker.click"
    customer_id = fields.Char(string="Kundnummer")

    @api.model
    def add_click(self, code, ip, country_code, stat_id=False):
        # Using sudo on all calls on self means we can always read and change things.
        # Care has to be taken on which data we store as not all users have sudo rights.
        # Some res.partners are protected, so we cannot store the actual record.
        self = self.sudo()
        res = super(LinkTrackerClick, self).add_click(code, ip, country_code, stat_id=stat_id)

        code_rec = self.env['link.tracker.code'].search([('code', '=', code)])
        if not code_rec:
            return None

        click = self.env['link.tracker.click'].search([('link_id', '=', code_rec.link_id.id),('ip', '=', ip)])
        if click:
            statistics = self.env['mail.mail.statistics'].search([('id', '=', stat_id)])
            receiver_model = statistics.model
            receiver_id = statistics.res_id
            statistics.total_clicks += 1
            if receiver_model == 'mail.mass_mailing.contact':
                #customer_id = self.env[receiver_model].browse(receiver_id).partner_id.customer_id utv12 code, should be removed
                customer_id = self.env[receiver_model].browse(receiver_id).email
            elif receiver_model == 'res.partner':
                customer_id = self.env[receiver_model].browse(receiver_id).customer_id
            else:
                msg = 'Unknown model: {receiver_model}'
                _logger.warning(msg.format(receiver_model=receiver_model))
                raise UserError(_(msg).format(receiver_model=receiver_model))

            click.customer_id = customer_id
            click.click_date = datetime.date.today()
            click.link_id.write({
                'user_clicks_per_link':
                    [(0, 0,
                      {
                          'click_date': fields.datetime.now(),
                          'ip': click.ip,
                          'country_id': click.country_id,
                          'customer_id': customer_id,
                      })]
            })
        return res
        
class MailMailStatistics(models.Model):
        _inherit = "mail.mail.statistics"
        total_clicks = fields.Integer()
