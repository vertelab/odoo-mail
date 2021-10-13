from odoo import models, fields, api, _
import datetime
from datetime import date
from odoo.tools.safe_eval import safe_eval
from dateutil import rrule
import pytz
import logging
_logger = logging.getLogger(__name__)

class Autoresponder(models.Model):
    _name = 'partner.event'
    _description = 'Autoresponder'
    _inherit = ['mail.thread']

    name = fields.Char(string="Autoresponder Segment")
    organizer_id = fields.Many2one('res.partner', string="Organizer")
    is_online = fields.Boolean('Online Event')
    address_id = fields.Many2one(
        'res.partner', string='Location',
        default=lambda self: self.env.user.company_id.partner_id,
        readonly=False, states={'done': [('readonly', True)]},
        track_visibility="onchange")
    country_id = fields.Many2one('res.country', 'Country', related='address_id.country_id', store=True, readonly=False)
    category = fields.Char(string="Category")
    user_id = fields.Many2one('res.users', string="Responsible", default=lambda self: self.env.user.id)
    date_begin = fields.Date(string="Start Date", required=True)
    date_end = fields.Date(string="End Date", required=True)
    creation_date = fields.Date(string="Creation Date", default=lambda self: self._context.get('date', fields.Date.context_today(self)))
    count_email_sent = fields.Integer(compute="count_total_email_sent", string="Email count")
    opened = fields.Float(string="Opened", default="95.0")

    def count_total_email_sent(self):

        for event in self:
            event.count_email_sent = len(self.env['event.email.audit'].search([('event_id','=',event.id)]).ids)

    @api.model
    def _prefill_email_schedule_ids(self):
        values = [
            (0, 0, {
                'template_id': self.env.ref('mass_mailing_autoresponder.meeting_reminder_email_template'),
                'interval_type': 'before_event',
                'interval_nbr': 1,
                'interval_unit': 'days'
            }),
            (0, 0, {
                'template_id': self.env.ref('mass_mailing_autoresponder.meeting_follow_up_email_template'),
                'interval_type': 'after_event',
                'interval_nbr': 3,
                'interval_unit': 'days'
            })]
        return values

    email_schedule_ids = fields.One2many('partner.event.email.schedule', 'partner_event_id',
                                         string="Email Schedule", default=_prefill_email_schedule_ids)
    state = fields.Selection([('draft', 'Draft'), ('running', 'Running'), ('end', 'End'),('cancelled', 'Cancelled') ],
                             default='draft')
    color = fields.Integer('Kanban Color Index')
    contact_domain = fields.Char(string="Search Filter")
    contact_domain_count = fields.Integer(string="Contact Count", compute='_compute_event_record')
    all_event_mail_count = fields.Integer(string="All Event Email Count", compute='_compute_event_record')
    today_event_mail_count = fields.Integer(string="Today's Email Count", compute='_compute_event_record')

    @api.depends('contact_domain')
    def _compute_event_record(self):
        for rec in self:
            if rec.contact_domain:
                domain = safe_eval(rec.contact_domain)
                res_ids = self.env['res.partner'].search(domain).ids
                rec.contact_domain_count = len(res_ids)

                # Get Today's Email Count
                today_event_mail_count = rec.env['mail.mail'].search([('model', '=', rec._name),
                                                                      ('res_id', '=', rec.id)])

                total_event_mail_count = []
                for _rec in today_event_mail_count:
                    if _rec.date.strftime("%Y-%m-%d") == datetime.datetime.today().strftime("%Y-%m-%d"):
                        total_event_mail_count.append(_rec)

                rec.today_event_mail_count = len(total_event_mail_count)

                # All Email sent for this event
                rec.all_event_mail_count = rec.env['mail.mail'].search_count([
                    ('res_id', '=', rec.id), ('model', '=', rec._name)])

    def update_autoresponder_status(self):
        for event in self.env['partner.event'].search([('state', '=', 'running')]):
            if event.date_end <= date.today():
                event.state = 'end'

    def automated_autoresponder_mail(self):

        event_ids = self.env['partner.event'].search([('state', '=', 'running')])
        for event in event_ids:
            for email_line in event.email_schedule_ids:
                if email_line.interval_type == 'after_event':
                    self.after_event(event, email_line, email_line.contact_ids)
                if email_line.interval_type == 'before_event':
                    self.before_event(event, email_line, email_line.contact_ids)

    def get_date_weekday_only(self, interval, contact_date):
        """
        Checks if there it's a weekend or holiday between contact date and
        returns date that is weekday instead.
        :param interval:
        :param contact_date:
        :return:
        """
        # Get all af holidays timezone adjusted
        af_holidays = [self.adjust_tz(d.date_from).date() for
                       d in
                       self.env['resource.calendar.leaves'].search([])]
        _datetime = contact_date
        i = 0
        # Add one day for every weekend day or holiday
        while i != interval:
            _datetime += datetime.timedelta(days=1)
            if not (_datetime.weekday() in (5, 6) or _datetime in af_holidays):
                i += 1
        return _datetime

    def after_event(self, event, email_line, contacts):
        today_date = self.adjust_tz(datetime.datetime.today()).strftime("%Y-%m-%d")
        domain = event.contact_domain and safe_eval(event.contact_domain) or []
        for contact in self.env['res.partner'].search(domain):
            if contact.id not in contacts.ids:
                week_day_date = False
                if email_line.interval_unit == 'days':
                    if email_line.ir_model_field:
                        contact_date = contact[str(email_line.ir_model_field.name)]
                        if contact_date:
                            _datetime = self.get_date_weekday_only(email_line.interval_nbr, contact_date)
                            week_day_date = list(rrule.rrule(rrule.DAILY,
                                                             dtstart=contact_date,
                                                             until=_datetime,
                                                             byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR)))
                    else:
                        _datetime = self.get_date_weekday_only(email_line.interval_nbr, event.date_begin)
                        week_day_date = list(rrule.rrule(rrule.DAILY, dtstart=event.date_begin, until=_datetime,
                                                         byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR)))

                    if week_day_date:
                        partner_comp_date = week_day_date[-1].strftime("%Y-%m-%d")
                        if partner_comp_date == today_date:
                            self._create_mail_campaign(contact, email_line)
                            # self._email_to_contacts(contact, event, email_line)
                            email_line.contact_ids = [(4, contact.id)]

    def before_event(self, event, email_line, contacts):
        today_date = datetime.datetime.today().strftime("%Y-%m-%d")
        domain = event.contact_domain and safe_eval(event.contact_domain) or []
        res_ids = self.env['res.partner'].search(domain).ids
        for contact_id in res_ids:
            if contact_id not in contacts.ids:
                if email_line.interval_unit == 'days':
                    partner_id = self.env['res.partner'].search([('id', '=', contact_id)])
                    if email_line.ir_model_field:
                        _datetime = self.get_date_weekday_only(email_line.interval_nbr, partner_id[str(email_line.ir_model_field.name)])
                        week_day_date = list(rrule.rrule(rrule.DAILY,
                                                         dtstart=_datetime,
                                                         until=partner_id[str(email_line.ir_model_field.name)],
                                                         byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR)))
                    else:
                        _datetime = self.get_date_weekday_only(email_line.interval_nbr, event.date_begin)

                        week_day_date = list(rrule.rrule(rrule.DAILY, dtstart=_datetime, until=event.date_begin,
                                                         byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR)))

                    if week_day_date:
                        if week_day_date[-1].strftime("%Y-%m-%d") == today_date:
                            self._create_mail_campaign(partner_id, email_line)
                            # self._email_to_contacts(partner_id, event, email_line)
                            email_line.contact_ids = [(4, partner_id.id)]

    def _create_mail_campaign(self, partner, event_line):
        partner_model = self.env['ir.model'].search([('model', '=', 'res.partner')], limit=1)
        name = event_line and \
               event_line.template_id and \
               event_line.template_id.name\
               or ""
        mailing_data = {
            'name':name,
            'user_id':self.env.user.id,
            'mailing_model_id':partner_model and partner_model.id or False,
            'mailing_domain': '%s' % [('email', 'in', [partner.email])],
            'body_html':event_line.template_id and event_line.template_id.body_html or False,
            'event_line_id':event_line.id,
            'auto_responder':True,
        }
        mailing_record = self.env['mail.mass_mailing'].create(mailing_data)
        mailing_record.put_in_queue()

    def _email_to_contacts(self, partner_id, event, email_line):
        audit_email = {
            'user_id': self.env.user.id,
            'partner_id': partner_id and partner_id.id or False,
            'sent_time': datetime.datetime.now(),
            'event_id': event.id,
            'event_line_id': email_line.id,
        }
        try:
            response_status = email_line.template_id.with_context(
                partner_email=partner_id.email, partner_lang=partner_id.lang
            ).send_mail(event.id, force_send=True)
            audit_email.update({
                'response':"Success Sent"
            })
            email_line.sent = True
        except:
            email_line.sent = False
            audit_email.update({
                'response': "Failed"
            })
            _logger.warning("Email sent is failed for the receipent %s with following email %s",partner_id.name,
                            partner_id.email)

        self.env['event.email.audit'].create(audit_email)

    def start_event(self):
        self.state = 'running'

    def button_cancel(self):
        self.state = 'cancelled'

    @staticmethod
    def adjust_tz(date, from_tz='utc', to_tz='Europe/Stockholm'):
        """Change between timezones."""
        if isinstance(date, str):
            date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
        to_tz = pytz.timezone(to_tz)
        return pytz.timezone(from_tz).localize(date).astimezone(to_tz).replace(tzinfo=None)


class EventEmailSchedule(models.Model):
    _name = 'partner.event.email.schedule'

    name = fields.Text(string='Description')
    template_id = fields.Many2one('mail.template', string="Email Template", domain=[('model', '=', 'partner.event')])
    partner_event_id = fields.Many2one('partner.event', string="Partner Event")
    contact_ids = fields.Many2many("res.partner","email_schedule_partner_rel","event_schedule_line_id","partner_id",
                                   string="Contacts")
    interval_nbr = fields.Integer('Interval', default=1)
    interval_unit = fields.Selection([
        ('days', 'Work Day(s)'),
        # ('weeks', 'Week(s)')
    ],
        string='Unit', default='days', required=True)
    interval_type = fields.Selection([
        ('before_event', 'Before the date'),
        ('after_event', 'After the date')],
        string='Trigger ', default="before_event", required=True)

    ir_model_field = fields.Many2one('ir.model.fields', string="Field", domain=[('model_id', '=', 'res.partner'),
                                                                                ('ttype', 'in', ['date', 'datetime'])])

    # sent = fields.Boolean('Sent', readonly=True)

    #statistics fields
    mail_massmailing_ids = fields.One2many("mail.mass_mailing", "event_line_id", string="Mass Mailing")
    sent = fields.Integer('Sent', compute="_compute_statistics_info")
    received = fields.Integer("Delivered Email", compute="_compute_statistics_info")
    opened = fields.Integer("Opened Email", compute="_compute_statistics_info")
    replied = fields.Integer("Replied Email", compute="_compute_statistics_info")
    bounced = fields.Integer("Bounced Email", compute="_compute_statistics_info")
    received_ratio = fields.Char("Delivered Ratio", compute="_compute_statistic_ratio")
    opened_ratio = fields.Char("Opened Ratio", compute="_compute_statistic_ratio")
    replied_ratio = fields.Char("Replied Ratio", compute="_compute_statistic_ratio")
    bounced_ratio = fields.Char("Bounced Ratio", compute="_compute_statistic_ratio")
    total = fields.Integer("Total", compute="_compute_total_camp")
    received_info = fields.Char("Delivered", compute="_compute_line_statistics")
    opened_info = fields.Char("Opened", compute="_compute_line_statistics")
    replied_info = fields.Char("Replied", compute="_compute_line_statistics")
    bounced_info = fields.Char("Bounced", compute="_compute_line_statistics")

    @api.multi
    def _compute_line_statistics(self):
        for event_line in self:
            received_line = str(event_line.received)
            received_line += "/"
            received_line += str(event_line.total)
            received_line += " ("
            received_line += str(event_line.received_ratio)
            received_line += " %)"
            event_line.received_info = received_line

            opened_line = str(event_line.opened)
            opened_line += "/"
            opened_line += str(event_line.total)
            opened_line += " ("
            opened_line += str(event_line.opened_ratio)
            opened_line += " %)"
            event_line.opened_info = opened_line

            replied_line = str(event_line.replied)
            replied_line += "/"
            replied_line += str(event_line.total)
            replied_line += " ("
            replied_line += str(event_line.replied_ratio)
            replied_line += " %)"
            event_line.replied_info = replied_line

            bounced_line = str(event_line.bounced)
            bounced_line += "/"
            bounced_line += str(event_line.total)
            bounced_line += " ("
            bounced_line += str(event_line.bounced_ratio)
            bounced_line += " %)"
            event_line.bounced_info = bounced_line



    @api.multi
    def _compute_total_camp(self):

        for event_line in self:
            event_line.total = len(event_line.mail_massmailing_ids.ids)

    @api.multi
    def _compute_statistic_ratio(self):
        for event_line in self:
            total = len(event_line.mail_massmailing_ids.ids)
            if total>0:
                event_line.delivered = event_line.sent - event_line.bounced
                event_line.received_ratio = 100.0 * event_line.delivered /total
                event_line.opened_ratio = 100.0 * event_line.opened/ total
                event_line.replied_ratio = 100.0 * event_line.replied /total
                event_line.bounced_ratio = 100.0 * event_line.bounced /total
            else:
                event_line.delivered = 0
                event_line.received_ratio = 0
                event_line.opened_ratio = 0
                event_line.replied_ratio = 0
                event_line.bounced_ratio = 0

    @api.multi
    def _compute_statistics_info(self):

        for event_line in self:
            sent = 0
            received = 0
            opened = 0
            replied = 0
            bounced = 0
            for mailing_info in event_line.mail_massmailing_ids:
                received += mailing_info.delivered
                opened += mailing_info.opened
                replied += mailing_info.replied
                bounced += mailing_info.bounced
                sent += mailing_info.sent
            event_line.received = received
            event_line.opened = opened
            event_line.replied = replied
            event_line.bounced = bounced
            event_line.sent = sent

class MailMassMailing(models.Model):

    _inherit = 'mail.mass_mailing'

    auto_responder = fields.Boolean("Auto Responder")
    event_line_id = fields.Many2one("partner.event.email.schedule", "Event Line")
