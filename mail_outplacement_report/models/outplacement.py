from odoo import models, api, _, fields
from datetime import datetime, timedelta, date
import logging

_logger = logging.getLogger(__name__)

# LOCAL_TZ: Local timezone 
LOCAL_TZ = 'Europe/Stockholm'

class HrEmployee(models.Model):
    _inherit = "hr.employee"
    def action_send_email(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        _logger.warn("DAER: ir_model_data: %s" % ir_model_data)
        try:
            
            template_id = ir_model_data.get_object_reference('mail_outplacement_report', 'email_template_login_employee')[1]
            _logger.warn("DAER: template_id1: %s" % template_id)
        except ValueError:
            template_id = False
            _logger.warn("DAER: template_id: %s" % template_id)
        template_browse =self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)
        _logger.warn("DAER: template_browse: %s" % template_browse)

class Outplacement(models.Model):
    _inherit = "outplacement"
    venue = fields.Text(string="Performing adress", help="Venue for meeting")
    date = fields.Date(string="Meeting date", help="Date of meeting")
    time = fields.Float(string="Meeting time")
    performing_operation_id = fields.Many2one(
        comodel_name='performing.operation',
        string='Performing Op',
        group_expand='_read_group_performing_operation_ids',)
    # performing_operation_adress = fields.Many2one(
    #     comodel_name='performing.operation',
    #     name = 'partner_ids.display_name',
    #     string='Performing ADDRESS', )
    performing_operation_adress = fields.Many2one(
        comodel_name ='res.partner',
        name='Adress', string='Performing Adress') 
    #performing_operation_ka_nr = fields.Integer(related="performing_operation_id.ka_nr", readonly=False, string='Performing DD',)
    #performing_operation_name = fields.Char(related="performing_operation_id.partner_ids.", string='Performing DD',)


    @api.multi
    def action_send_eletter(self):
        template_id = self.env.ref('mail_outplacement_report.email_template_assigned_coach').id
        _logger.warn("ALDIN: template_id1: %s" % template_id)
        template = self.env['mail.template'].browse(template_id)
        
        _logger.warn("ALDIN: template: %s" % template)
        _logger.warn("ALDIN: self: %s" % self)
        result = template.send_mail(self.id, force_send=True)
        _logger.warn("ALDIN: result: %s" % result)
        
        
