from odoo import api, models, fields, _

class MassMailing(models.Model):

    _inherit = "mail.mass_mailing"

    keep_archives = fields.Boolean(string='Keep Archives', default=True, required=True)

class MassMailingMessages(models.Model):

    _name = "mass.mailing.message"
    _description = "Mass Mailing Message"
    _rec_name = "mass_mailing_id"

    document = fields.Reference(string='Document', selection='_selection_target_model',
        compute='_compute_resource_ref')
    model = fields.Char("Document Model")
    res_id = fields.Char("Document ID")
    mass_mailing_id = fields.Many2one("mail.mass_mailing", string="Mailing")
    statistic_id = fields.Many2one("mail.mail.statistics", string="Statistic")
    sent_date = fields.Datetime("Sent")
    clicked = fields.Datetime("Clicked", related='statistic_id.clicked')
    bounced = fields.Datetime("Bounced", related='statistic_id.bounced')
    opened = fields.Datetime("Opened", related='statistic_id.opened')
    replied = fields.Datetime("Replied", related='statistic_id.replied')
    partner_id = fields.Many2one('res.partner', "Contact")

    @api.multi
    def open_email(self):
        self.ensure_one()
        mail_obj = self.env['mail.mail']
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        action_id = self.env.ref('mail.action_view_mail_mail').id
        menu_id = self.env.ref('base.menu_email').id
        for rec in self:
            if rec.res_id and rec.model and rec.mass_mailing_id:
                mail = mail_obj.search([('res_id', '=', rec.res_id), ('model', '=', rec.model),
                                        ('mailing_id', '=', rec.mass_mailing_id.id), ('state', '=', 'sent')], limit=1)
                if mail:
                    url = base_url + '#id=' + str(mail.id) +'&action=' + str(action_id) + \
                          '&model=mail.mail&view_type=form&menu_id=' + str(menu_id)
                    return {
                        'type': 'ir.actions.act_url',
                        'target': 'new',
                        'url': url,
                    }

    @api.model
    def _selection_target_model(self):
        models = self.env['ir.model'].search([])
        return [(model.model, model.name) for model in models]

    def _compute_resource_ref(self):
        for record in self:
            if record.res_id and record.model:
                record.document = '%s,%s' % (record.model, record.res_id)
            else:
                record.document = False

class ResPartner(models.Model):
    _inherit = 'res.partner'

    mail_message_ids = fields.One2many("mass.mailing.message", 'partner_id', "Mass mailing Messages")

class MailStatistics(models.Model):

    _inherit = "mail.mail.statistics"

    @api.model
    def write(self, vals):
        res = super(MailStatistics, self).write(vals)
        if vals.get("sent"):
            for rec in self:
                if rec.res_id and rec.model and rec.sent and rec.mass_mailing_id:
                    if rec.model == 'sale.order':
                        sale_order = self.env['sale.order'].search([('id', '=', int(rec.res_id))])
                        if sale_order:
                            partner = sale_order.partner_id
                            partner.mail_message_ids = [(0, 0, {
                                'res_id': rec.res_id,
                                'model': rec.model,
                                'sent_date': rec.sent,
                                'mass_mailing_id': rec.mass_mailing_id.id,
                                'statistic_id': rec.id
                            })]
                    elif rec.model == 'crm.lead':
                        lead = self.env['crm.lead'].search([('id', '=', int(rec.res_id))])
                        if lead and lead.partner_id:
                            partner = lead.partner_id
                            partner.mail_message_ids = [(0, 0, {
                                'res_id': rec.res_id,
                                'model': rec.model,
                                'sent_date': rec.sent,
                                'mass_mailing_id': rec.mass_mailing_id.id,
                                'statistic_id': rec.id
                            })]
                    elif rec.model == 'res.partner':
                        partner = self.env['res.partner'].browse(int(rec.res_id))
                        if partner:
                            partner.mail_message_ids = [(0, 0, {
                                'res_id': rec.res_id,
                                'model': rec.model,
                                'sent_date': rec.sent,
                                'mass_mailing_id': rec.mass_mailing_id.id,
                                'statistic_id': rec.id
                            })]
        return res
