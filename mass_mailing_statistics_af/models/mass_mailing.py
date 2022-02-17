from odoo import api, fields, models

class MassMailing(models.Model):
    _inherit = 'mail.mass_mailing'

    received = fields.Integer("Received", compute='_compute_statistics')
    opened = fields.Integer("Opened", compute='_compute_statistics')
    replied = fields.Integer("Replied", compute='_compute_statistics')
    bounced = fields.Integer("Bounced", compute='_compute_statistics')
    clicks = fields.Integer("Clicked", compute='_compute_statistics', help="Number of mails where atleast one link was clicked" )
    total_clicks = fields.Integer("Total Clicks", compute='_compute_statistics', help="Everytime a link is clicked")
    clicks_ratio = fields.Integer(string="Click frequency", compute='_compute_statistics', help="Is the number of mails sent divided by the number of mails where atleast one link was clicked" ) # Already exists in core, is redefined here since the orignal string is "Number of click" which it is wrong
    clicks_ratio_percentage = fields.Char(compute='_compute_clicks_ratio_percentage')
    ctor = fields.Integer(compute='_compute_statistics', help="Number of mails where at least one link is clicked divided by the number of unique opened mails")
    ctor_percentage = fields.Char("CTOR", compute='_compute_ctor_percentage')
    opened_ratio_percentage = fields.Char(string="OR", compute='_compute_opened_ratio_percentage')

    def _compute_statistics(self):
        """ Compute statistics of the mass mailing """
        self.env.cr.execute("""
               SELECT
                   m.id as mailing_id,
                   COUNT(s.id) AS expected,
                   COUNT(CASE WHEN s.sent is not null THEN 1 ELSE null END) AS sent,
                   COUNT(CASE WHEN s.scheduled is not null AND s.sent is null AND s.exception is null AND s.ignored is null THEN 1 ELSE null END) AS scheduled,
                   COUNT(CASE WHEN s.scheduled is not null AND s.sent is null AND s.exception is not null THEN 1 ELSE null END) AS failed,
                   COUNT(CASE WHEN s.scheduled is not null AND s.sent is null AND s.exception is null AND s.ignored is not null THEN 1 ELSE null END) AS ignored,
                   COUNT(CASE WHEN s.sent is not null AND s.bounced is null THEN 1 ELSE null END) AS received,
                   COUNT(CASE WHEN s.opened is not null THEN 1 ELSE null END) AS opened,
                   COUNT(CASE WHEN s.clicked is not null THEN 1 ELSE null END) AS clicks,
                   SUM(s.total_clicks) AS total_clicks,
                   COUNT(CASE WHEN s.replied is not null THEN 1 ELSE null END) AS replied,
                   COUNT(CASE WHEN s.bounced is not null THEN 1 ELSE null END) AS bounced,
                   COUNT(CASE WHEN s.exception is not null THEN 1 ELSE null END) AS failed
               FROM
                   mail_mail_statistics s
               RIGHT JOIN
                   mail_mass_mailing m
                   ON (m.id = s.mass_mailing_id)
               WHERE
                   m.id IN %s
               GROUP BY
                   m.id
           """, (tuple(self.ids),))
        for row in self.env.cr.dictfetchall():
            total = row['expected'] = (row['expected'] - row['ignored'])
            if total != 0:
                row['received_ratio'] = 100.0 * row['received'] / total
            if row['received'] != 0:
                row['opened_ratio'] = 100.0 * row['opened'] / row['received']
                row['replied_ratio'] = 100.0 * row['replied'] / total
                row['bounced_ratio'] = 100.0 * row['bounced'] / total
            if row['opened'] != 0:
                row['ctor'] = 100.0 * row['clicks'] / row['opened']
            if row['received'] != 0:
                row['clicks_ratio'] = 100.0 * row['clicks'] / row['received']
            self.browse(row.pop('mailing_id')).update(row)

    def _compute_clicks_ratio_percentage(self):
        for rec in self:
            rec.clicks_ratio_percentage = f"{rec.clicks_ratio} %"

    def _compute_ctor_percentage(self):
        for rec in self:
            rec.ctor_percentage = f"{rec.ctor} %"

    def _compute_opened_ratio_percentage(self):
        for rec in self:
            rec.opened_ratio_percentage = f"{rec.opened_ratio} %"

