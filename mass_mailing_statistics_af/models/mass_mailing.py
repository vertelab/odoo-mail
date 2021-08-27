from odoo import api, fields, models

class MassMailing(models.Model):
    _inherit = 'mail.mass_mailing'

    received = fields.Integer("Received", compute='_compute_statistics')
    opened = fields.Integer("Opened", compute='_compute_statistics')
    replied = fields.Integer("Replied", compute='_compute_statistics')
    bounced = fields.Integer("Bounced", compute='_compute_statistics')
    clicks = fields.Integer("Clicks", compute='_compute_statistics')

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
                   COUNT(CASE WHEN s.sent is not null AND s.bounced is null THEN 1 ELSE null END) AS delivered,
                   COUNT(CASE WHEN s.opened is not null THEN 1 ELSE null END) AS opened,
                   COUNT(CASE WHEN s.clicked is not null THEN 1 ELSE null END) AS clicked,
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
            total = row['expected'] = (row['expected'] - row['ignored']) or 1
            row['received_ratio'] = 100.0 * row['delivered'] / total
            row['received'] = row['delivered']
            row['opened_ratio'] = 100.0 * row['opened'] / total
            row['opened'] = row['opened']
            row['clicks_ratio'] = 100.0 * row['clicked'] / total
            row['clicks'] = 100.0 * row['clicked'] / total
            row['replied_ratio'] = 100.0 * row['replied'] / total
            row['replied'] = row['replied']
            row['bounced_ratio'] = 100.0 * row['bounced'] / total
            row['bounced'] = row['bounced']
            self.browse(row.pop('mailing_id')).update(row)