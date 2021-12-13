from odoo import api, fields, models, tools
from odoo.tools import email_re

class MailComposeMessage(models.TransientModel):
    """Add concept of mass mailing campaign to the mail.compose.message wizard
    """
    _inherit = 'mail.compose.message'

    @api.multi
    def get_mail_values(self, res_ids):
        """ Override method that generated the mail content by creating the
        mail.mail.statistics values in the o2m of mail_mail, when doing pure
        email mass mailing. """
        self.ensure_one()
        res = super(MailComposeMessage, self).get_mail_values(res_ids)
        # Preprocess res.partners to batch-fetch from db
        # if recipient_ids is present, it means they are partners
        # (the only object to fill get_default_recipient this way)
        recipient_partners_ids = []
        read_partners = {}
        for res_id in res.keys():
            mail_values = res[res_id]
            mail_values['state'] = 'outgoing'
            if mail_values.get('recipient_ids'):
                # recipient_ids is a list of x2m command tuples at this point
                recipient_partners_ids.append(mail_values.get('recipient_ids')[0][1])
        read_partners = self.env['res.partner'].browse(recipient_partners_ids)

        partners_email = {p.id: p.email for p in read_partners}

        opt_out_list = self._context.get('mass_mailing_opt_out_list')
        for res_id in res.keys():
            mail_values = res[res_id]
            if mail_values.get('email_to'):
                recips = tools.email_split(mail_values['email_to'])
            else:
                partner_id = (mail_values.get('recipient_ids') or [(False, '')])[0][1]
                recips = tools.email_split(partners_email.get(partner_id))
            mail_to = recips[0].lower() if recips else False
            if (opt_out_list and mail_to in opt_out_list) or (not mail_to or not email_re.findall(mail_to)):
                # prevent sending to blocked addresses that were included by mistake
                mail_values['state'] = 'cancel'
        return res
