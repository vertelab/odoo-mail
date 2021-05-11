from odoo import models, fields, api, _


class MassMailing(models.Model):
    _name = 'mail.mass_mailing'
    _inherits = {'utm.source': 'source_id'}
    _inherit = ['mail.mass_mailing', 'mail.thread', 'mail.activity.mixin']

    email_from = fields.Char(string='From', required=True,
        default=lambda self: self.env['mail.message']._get_default_from(), track_visibility='onchange')

    @api.model
    def create(self, vals):
        res = super(MassMailing, self).create(vals)
        mail_msg_obj = self.env['mail.message']
        if res.state == 'draft':
            msg = """<div class='o_thread_message_content'> <ul class='o_mail_thread_message_tracking'>        
                                            <li>
                                                Status:
                                                    <span> Draft </span>
                                            </li>
                                    </ul>
                                </div>"""
            mail_msg_obj.create({
                'model': 'mail.mass_mailing', 'res_id': res.id,
                'body': msg
            })
        return res

    @api.multi
    def write(self, vals):
        res = super(MassMailing, self).write(vals)
        if vals.get('state') and vals.get('state') in ('in_queue', 'draft'):
            mail_msg_obj = self.env['mail.message']
            if vals.get('state') == 'in_queue':
                for mass_mail in self:
                    msg = """<div class='o_thread_message_content'> <ul class='o_mail_thread_message_tracking'>        
                                <li>
                                    Status:
                                        <span> Draft </span>
                                        <span aria-label='Changed' class='fa fa-long-arrow-right' role='img' title='Changed'></span>
                                    <span>
                                        In Queue
                                    </span>
                                </li>
                            
                        </ul>
                    </div>"""
                    mail_msg_obj.create({
                        'model': 'mail.mass_mailing', 'res_id': mass_mail.id,
                        'body': msg
                    })
            elif vals.get('state') == 'draft':
                for mass_mail in self:
                    msg = """<div class='o_thread_message_content'> <ul class='o_mail_thread_message_tracking'>        
                                <li>
                                    Status:
                                        <span> In Queue </span>
                                        <span aria-label='Changed' class='fa fa-long-arrow-right' role='img' title='Changed'></span>
                                    <span>
                                        Draft
                                    </span>
                                </li>

                        </ul>
                    </div>"""
                    mail_msg_obj.create({
                        'model': 'mail.mass_mailing', 'res_id': mass_mail.id,
                        'body': msg
                    })
        return res
