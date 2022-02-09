
from odoo import api, fields, models, tools

class MassMailing(models.Model):
    _inherit = 'mail.statistics.report'
    
    clicks_ratio = fields.Float(readonly=True, group_operator="avg")
    total_clicks = fields.Integer(readonly=True)
    @api.model_cr
    def init(self):
        """Mass Mail Statistical Report: based on mail.mail.statistics that models the various
        statistics collected for each mailing, and mail.mass_mailing model that models the
        various mailing performed. """
        tools.drop_view_if_exists(self.env.cr, 'mail_statistics_report')
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW mail_statistics_report AS (
                SELECT
                    min(ms.id) as id,
                    ms.scheduled as scheduled_date,
                    utm_source.name as name,
                    utm_campaign.name as campaign,
                    count(ms.bounced) as bounced,
                    count(ms.sent) as sent,
                    (count(ms.sent) - count(ms.bounced)) as delivered,
                    count(ms.opened) as opened,
                    count(ms.replied) as replied,
                    count(ms.clicked) as clicked,
                    count(ms.total_clicks) as total_clicks,
                    (((1.0 * count(ms.clicked)) / nullif((1.0 * count(ms.sent)),0)) * 100)  as clicks_ratio,
                    mm.state,
                    mm.email_from
                FROM
                    mail_mail_statistics as ms
                    left join mail_mass_mailing as mm ON (ms.mass_mailing_id=mm.id)
                    left join mail_mass_mailing_campaign as mc ON (ms.mass_mailing_campaign_id=mc.id)
                    left join utm_campaign as utm_campaign ON (mc.campaign_id = utm_campaign.id)
                    left join utm_source as utm_source ON (mm.source_id = utm_source.id)
                GROUP BY ms.scheduled, utm_source.name, utm_campaign.name, mm.state, mm.email_from
            )""")
