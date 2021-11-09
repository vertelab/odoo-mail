# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import datetime
import random
import re
import string
import requests
from lxml import html
from werkzeug import urls, utils
from odoo import models, fields, api, _
from odoo.tools import ustr
URL_REGEX = r'(\bhref=[\'"](?!mailto:|tel:|sms:)([^\'"]+)[\'"])'
import logging
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
            'name':'Indevidual Clicks',
            'type':'ir.actions.act_window',
            'res_model':'link.tracker.click',
            'view_type':'form',
            'view_mode': 'tree',
            'domain': [('id', 'in', self.link_click_ids.mapped('id'))],
            'view_id': tree_view_id,
            'res_id': False,
            'context': False,
            'target':'new',
        }
    @api.multi
    def action_individual_clicks_tree_view(self):
        tree_view_id = self.env.ref('mass_mailing_sender_logs.view_link_tracker_click_tree').id
        return {
            'name':'Individual Clicks',
            'type':'ir.actions.act_window',
            'res_model':'link.tracker.click.user.clicks.per.link',
            'view_type':'form',
            'view_mode': 'tree',
            'domain': [('id', 'in', self.user_clicks_per_link.mapped('id'))],
            'view_id': tree_view_id,
            'res_id': False,
            'context': False,
            'target':'new',
        }
#Used to track each time a a mail_receiver clicks the same link.
#In order to keep track of the date of each click we create a new one each time a user clicks a link.
class LinkTrackerClickUserClicks(models.Model):
    _name = "link.tracker.click.user.clicks.per.link"
    click_date = fields.Datetime(string='Create Date')
    ip = fields.Char(string='Internet Protocol')
    country_id = fields.Many2one('res.country', 'Country')
    mail_receiver_id = fields.Reference (selection = [('mail.mass_mailing.contact', 'Mail Contact'), ('res.users', 'Res User')],  string = "Source Document")
    link_tracker_id = fields.Many2one('link.tracker', 'Link Tracker', required=True, ondelete='cascade')
class LinkTrackerClick(models.Model):
    _inherit = "link.tracker.click"
    mail_receiver_id = fields.Reference (selection = [('mail.mass_mailing.contact', 'Mail Contact'), ('res.users', 'Res User')],  string = "Source Document")
    @api.model
    def add_click(self, code, ip, country_code, stat_id=False):
        self = self.sudo()
        res = super(LinkTrackerClick, self).add_click(code, ip, country_code, stat_id=stat_id)
        code_rec = self.env['link.tracker.code'].search([('code', '=', code)])
        if not code_rec:
            return None
        click= self.env['link.tracker.click'].search([('link_id', '=', code_rec.link_id.id),('ip', '=', ip)])
        if click:
            statistics = self.env['mail.mail.statistics'].search([('id', '=', stat_id)])
            receiver_model =  statistics.model
            receiver_id = statistics.res_id
            receiver_id_model = f'{receiver_model},{receiver_id}'
            click.mail_receiver_id = receiver_id_model
            click.click_date = datetime.date.today()
            click.link_id.write({
                'user_clicks_per_link':
                    [(0,0,
                      {
                          'click_date':fields.datetime.now(),
                          'ip':click.ip,
                          'country_id':click.country_id,
                          'mail_receiver_id':receiver_id_model,
                      })]
            })
        return res