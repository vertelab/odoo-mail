import logging

from odoo import api, fields, models, tools

_logger = logging.getLogger(__name__)


class MassMailing(models.Model):
    _inherit = 'mail.statistics.report'
    
    clicks_ratio = fields.Float(readonly=True, group_operator="avg")
    total_clicks = fields.Integer(readonly=True)
    ctor = fields.Float(string="CTOR", readonly=True, group_operator="avg")
    opened_ratio = fields.Float(readonly=True, group_operator="avg")

    @api.model_cr
    def init(self):
        """
        Mass Mail Statistical Report: based on mail.mail.statistics
        that models the various statistics collected for each mailing,
        and mail.mass_mailing model that models the various mailing
        performed.
        """
        self = self.sudo()
        tools.drop_view_if_exists(self.env.cr, 'mail_statistics_report')
        # ToDo: mm.sent_date as scheduled_date should be as sent_date?,
        # ToDo: but needs testing and checks that it dont break anything.
        # This data can be pretty large if a lot of mailings is done over time,
        # Maybe consider to restrict how old data we pull in this query.
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW mail_statistics_report AS (
                SELECT
                    min(ms.id) as id,
                    mm.sent_date as scheduled_date,
                    utm_source.name as name,
                    utm_campaign.name as campaign,
                    count(ms.bounced) as bounced,
                    count(ms.sent) as sent,
                    (count(ms.sent) - count(ms.bounced)) as delivered,
                    count(ms.opened) as opened,
                    count(ms.replied) as replied,
                    count(ms.clicked) as clicked,
                    sum(ms.total_clicks) as total_clicks,
                    CAST(count(ms.clicked) AS FLOAT) / nullif(count(ms.sent) - count(ms.bounced), 0) as clicks_ratio,
                    CAST(count(ms.clicked) AS FLOAT) / nullif(count(ms.opened), 0) as ctor,
                    CAST(count(ms.opened) AS FLOAT) / nullif(count(ms.sent) - count(ms.bounced), 0) as opened_ratio,
                    mm.state,
                    mm.email_from
                FROM
                    mail_mail_statistics as ms
                    left join mail_mass_mailing as mm ON (ms.mass_mailing_id=mm.id)
                    left join mail_mass_mailing_campaign as mc ON (ms.mass_mailing_campaign_id=mc.id)
                    left join utm_campaign as utm_campaign ON (mc.campaign_id = utm_campaign.id)
                    left join utm_source as utm_source ON (mm.source_id = utm_source.id)
                -- Avoid to group on values from ms, as it can break calculations.
                GROUP BY mm.sent_date, utm_source.name, utm_campaign.name, mm.state, mm.email_from
            )""")
