from odoo import models

class MassMailing(models.Model):
    _inherit = 'mail.mass_mailing'

    # Overwrite mass mainling method to show different list view from smart buttons
    def _action_view_documents_filtered(self, view_filter):
        if view_filter in ('sent', 'opened', 'replied', 'bounced', 'clicked'):
            opened_stats = self.statistics_ids.filtered(lambda stat: stat[view_filter])
        elif view_filter == ('delivered'):
            opened_stats = self.statistics_ids.filtered(lambda stat: stat.sent and not stat.bounced)
        else:
            opened_stats = self.env['mail.mail.statistics']
        res_ids = opened_stats.mapped('res_id')
        model_name = self.env['ir.model']._get(self.mailing_model_real).display_name
        if self.mailing_model_real == 'res.partner':
            view_ref = self.env['ir.model.data'].get_object_reference('mail_mass_mailing_gdrp_limitations',
                                                                      'contact_tree_view_for_email_marketing')
            view_id = view_ref and view_ref[1] or False,
            return {
                'name': model_name,
                'type': 'ir.actions.act_window',
                'view_mode': 'tree',
                'res_model': self.mailing_model_real,
                'domain': [('id', 'in', res_ids)],
                'view_id': view_id,
            }
        else:
            return {
                'name': model_name,
                'type': 'ir.actions.act_window',
                'view_mode': 'tree',
                'res_model': self.mailing_model_real,
                'domain': [('id', 'in', res_ids)],
            }