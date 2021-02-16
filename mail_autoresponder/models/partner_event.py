from odoo import models, fields, api, _
import datetime
from odoo.tools.safe_eval import safe_eval


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

    state = fields.Selection([('draft', 'Draft'), ('running', 'Running'), ('canceled', 'Cancelled')], default='draft')
    color = fields.Integer('Kanban Color Index')

    contact_domain = fields.Char(string="Search Filter")

    def automated_event_mail(self):
        # event_ids = self.env['partner.event'].search([('state', '=', 'running')])
        event_ids = self.env['partner.event'].search([])
        for event in event_ids:
            for email_line in event.email_schedule_ids:
                if email_line.interval_type == 'after_event' and not email_line.sent:
                    self.after_event(event, email_line)

                if email_line.interval_type == 'before_event' and not email_line.sent:
                    self.before_event(event, email_line)

    def after_event(self, event, email_line):
        today_date = datetime.datetime.today().strftime("%Y-%m-%d")

        domain = safe_eval(event.contact_domain)
        res_ids = self.env['res.partner'].search(domain).ids

        for contact_id in res_ids:
            if email_line.interval_unit == 'days':
                partner_id = self.env['res.partner'].search([('id', '=', contact_id)])
                if email_line.ir_model_field:
                    _datetime = partner_id[str(email_line.ir_model_field.name)] + datetime.timedelta(
                        days=email_line.interval_nbr)
                else:
                    _datetime = event.date_begin + datetime.timedelta(days=email_line.interval_nbr)
                _date = _datetime.strftime("%Y-%m-%d")
                if _date == today_date:
                    self._email_to_contacts(partner_id, event, email_line)

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
                else:
                    _datetime = event.date_begin - datetime.timedelta(days=email_line.interval_nbr)
                _date = _datetime.strftime("%Y-%m-%d")
                if _date == today_date:
                    self._email_to_contacts(partner_id, event, email_line)

    def _email_to_contacts(self, partner_id, event, email_line):
        email_line.template_id.with_context(
            partner_email=partner_id.email, partner_lang=partner_id.lang
        ).send_mail(event.id, force_send=True)
        email_line.sent = True

    def start_event(self):
        self.state = 'running'

    def button_cancel(self):
        self.state = 'canceled'


class EventEmailSchedule(models.Model):
    _name = 'partner.event.email.schedule'

    name = fields.Text(string='Description')
    template_id = fields.Many2one('mail.template', string="Email Template", domain=[('model', '=', 'partner.event')])

    partner_event_id = fields.Many2one('partner.event', string="Partner Event")

    interval_nbr = fields.Integer('Interval', default=1)
    interval_unit = fields.Selection([
        ('days', 'Day(s)'),
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
