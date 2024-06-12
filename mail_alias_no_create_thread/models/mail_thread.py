from odoo import models, fields, api, tools
import logging

_logger = logging.getLogger(__name__)

class MailThread(models.AbstractModel):
    
    _inherit = "mail.thread"

    @api.model
    def message_route(self, message, message_dict, model=None, thread_id=None, custom_values=None):

        recipients = tools.email_split(message_dict["recipients"])

        mail_alias_ids = []        

        for recipient in recipients:

            recipient = recipient.split("@")[0]
            mail_alias_ids_domain = [("alias_name", "=", recipient)]
            mail_alias_ids.append(self.env["mail.alias"].search(mail_alias_ids_domain))

        for mail_alias_id in mail_alias_ids:
            
            if mail_alias_id.no_message_on_replay == True:

                message_dict['references'] = False
                message_dict['in_reply_to'] = ""
 
        res = super().message_route(message, message_dict, model, thread_id, custom_values)

        return res