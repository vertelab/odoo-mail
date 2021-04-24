from odoo import models, fields, api, _
import datetime
from datetime import date
from odoo.tools.safe_eval import safe_eval
from dateutil import rrule
import logging
_logger = logging.getLogger(__name__)

class PartnerEvent(models.Model):
    _name = 'partner.event'
    _description = 'Customer Dialogue'
    _inherit = ['mail.thread']

    name = fields.Char(string="Event Segment")
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

    def count_total_email_sent(self):

        for event in self:
            event.count_email_sent = len(self.env['event.email.audit'].search([('event_id','=',event.id)]).ids)

    @api.model
    def _prefill_email_schedule_ids(self):
        values = [
            (0, 0, {
                'template_id': self.env.ref('mail_autoresponder.meeting_reminder_email_template'),
                'interval_type': 'before_event',
                'interval_nbr': 1,
                'interval_unit': 'days'
            }),
            (0, 0, {
                'template_id': self.env.ref('mail_autoresponder.meeting_follow_up_email_template'),
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

    def update_event_status(self):
        for event in self.env['partner.event'].search([('state', '=', 'running')]):
            if event.date_end <= date.today():
                event.state = 'end'


    def automated_event_mail(self):

        event_ids = self.env['partner.event'].search([('state', '=', 'running')])
        for event in event_ids:
            for email_line in event.email_schedule_ids:
                if email_line.interval_type == 'after_event' and not email_line.sent:
                    self.after_event(event, email_line)
                if email_line.interval_type == 'before_event' and not email_line.sent:
                    print ("It's here!")
                    self.before_event(event, email_line)

    def after_event(self, event, email_line):
        today_date = datetime.datetime.today().strftime("%Y-%m-%d")
        domain = safe_eval(event.contact_domain)
        for contact in self.env['res.partner'].search(domain):
            week_day_date = False
            if email_line.interval_unit == 'days':
                if email_line.ir_model_field:
                    contact_date = contact[str(email_line.ir_model_field.name)]
                    if contact_date:
                        _datetime = contact_date + datetime.timedelta(
                            days=email_line.interval_nbr)
                        week_day_date = list(rrule.rrule(rrule.DAILY,
                                                         dtstart=contact_date,
                                                         until=_datetime,
                                                         byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR)))
                else:
                    _datetime = event.date_begin + datetime.timedelta(days=email_line.interval_nbr)
                    week_day_date = list(rrule.rrule(rrule.DAILY, dtstart=event.date_begin, until=_datetime,
                                                     byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR)))

                if week_day_date:
                    partner_comp_date = week_day_date[-1].strftime("%Y-%m-%d")
                    if partner_comp_date == today_date:
                        self._email_to_contacts(contact, event, email_line)

    def before_event(self, event, email_line):
        today_date = datetime.datetime.today().strftime("%Y-%m-%d")
        domain = safe_eval(event.contact_domain)
        res_ids = self.env['res.partner'].search(domain).ids
        for contact_id in res_ids:
            if email_line.interval_unit == 'days':
                partner_id = self.env['res.partner'].search([('id', '=', contact_id)])
                if email_line.ir_model_field:
                    _datetime = partner_id[str(email_line.ir_model_field.name)] - datetime.timedelta(
                        days=email_line.interval_nbr)
                    week_day_date = list(rrule.rrule(rrule.DAILY,
                                                     dtstart=_datetime,
                                                     until=partner_id[str(email_line.ir_model_field.name)],
                                                     byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR)))
                else:
                    _datetime = event.date_begin - datetime.timedelta(days=email_line.interval_nbr)

                    week_day_date = list(rrule.rrule(rrule.DAILY, dtstart=_datetime, until=event.date_begin,
                                                     byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR)))
                if week_day_date:
                    if week_day_date[-1].strftime("%Y-%m-%d") == today_date:
                        self._email_to_contacts(partner_id, event, email_line)

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

class EventEmailSchedule(models.Model):
    _name = 'partner.event.email.schedule'

    name = fields.Text(string='Description')
    template_id = fields.Many2one('mail.template', string="Email Template", domain=[('model', '=', 'partner.event')])

    partner_event_id = fields.Many2one('partner.event', string="Partner Event")

    interval_nbr = fields.Integer('Interval', default=1)
    interval_unit = fields.Selection([
        ('days', 'Work Day(s)'),
        # ('weeks', 'Week(s)')
    ],
        string='Unit', default='days', required=True)
    interval_type = fields.Selection([
        ('before_event', 'Before the event'),
        ('after_event', 'After the event')],
        string='Trigger ', default="before_event", required=True)

    ir_model_field = fields.Many2one('ir.model.fields', string="Field", domain=[('model_id', '=', 'res.partner'),
                                                                                ('ttype', 'in', ['date', 'datetime'])])

    sent = fields.Boolean('Sent', readonly=True)
