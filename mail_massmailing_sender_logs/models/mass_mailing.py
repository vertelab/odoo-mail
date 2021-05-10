from odoo import models, fields, _

class MassMailing(models.Model):

    _name = 'mail.mass_mailing'
    _inherits = {'utm.source': 'source_id'}
    _inherit = ['mail.mass_mailing','mail.thread', 'mail.activity.mixin']

    state = fields.Selection([('draft', 'Draft'), ('in_queue', 'In Queue'), ('sending', 'Sending'), ('done', 'Sent')],
                             string='Status', required=True, copy=False, default='draft',
                             group_expand='_group_expand_states', track_visibility='onchange')

class MassMailingScheduleDate(models.TransientModel):
    _inherit = 'mass.mailing.schedule.date'

    def set_schedule_date(self):
        mail_msg_obj = self.env['mail.message']
        msg = _("Mailing - " + "<b> " + self.mass_mailing_id.name + "</b>" + " scheduled by " + self.env.user.name + " From " + \
                self.mass_mailing_id.email_from)
        mail_msg_obj.sudo().create({'model': 'mail.mass_mailing', 'res_id': self.mass_mailing_id.id,
                             'body': msg})
        self.mass_mailing_id.write({'schedule_date': self.schedule_date, 'state': 'in_queue'})
