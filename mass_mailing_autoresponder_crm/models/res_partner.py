from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    mail_adkd_campaign_ids = fields.Many2many(
        comodel_name='res.partner.mail.adkd.campaign',
        column1='partner_id',
        column2='mail_adkd_campaign_id',
        string='Campaigns')


class ResPartnerMailADKDCampaign(models.Model):
    _name = "res.partner.mail.adkd.campaign"
    _description = "Res Partner Mail ADKD Campaign"

    name = fields.Char(string="name")
    partner_ids = fields.Many2many(comodel_name='res.partner',
                                   column1='mail_adkd_campaign_id',
                                   column2='partner_id', string='Partners')