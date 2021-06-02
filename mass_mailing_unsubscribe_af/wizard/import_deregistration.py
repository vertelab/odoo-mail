import base64
import csv
import io
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from xlrd import open_workbook
from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class ImportDeregistratioFile(models.TransientModel):
    _name = 'import.deregistration.file'
    _description = 'Import Deregistration File'

    file = fields.Binary(string='File')
    filename = fields.Char(string='File name')

    def import_data(self):
        if not self.file or not \
                self.filename.lower().endswith(('.xls', '.xlsx', '.csv')):
            raise UserError(_("Please Select an .xls or .csv or its compatible file to Import."))
        unsub_obj = self.env['mail.unsubscription']
        mail_list_obj = self.env['mail.mass_mailing.contact']
        black_list_obj = self.env['mail.blacklist']
        partner_obj = self.env['res.partner']
        reason_obj = self.env['mail.unsubscription.reason']
        now = datetime.now() + timedelta(hours=2)
        if self.filename.lower().endswith('.csv'):
            data_list = []
            headers = []
            result_vals = []

            # Decode data to string
            csv_data = base64.b64decode(self.file)
            data_file = io.StringIO(csv_data.decode("utf-8"))
            # Read CSV
            csv_reader = csv.reader(data_file, delimiter=',')
            # Put rows to data list
            data_list.extend(csv_reader)
            # Set headers
            headers.extend(data_list[0])

            # Prepare values
            for row in data_list[1:]:
                result_dict = {}
                counter = 0
                for cell in row:
                    result_dict.update({headers[counter]: cell})
                    counter += 1
                result_vals.append(result_dict)
            correct_header = ['Email', 'Date', 'Reason']
            check_header = all(item in headers for item in correct_header)
            if not check_header:
                raise UserError(_("Please correct Header in file!"))
            else:
                for row in result_vals:
                    email = row.get('Email')
                    date = row.get('Date')
                    reason_val = row.get('Reason')
                    if date:
                        date = str(datetime.strptime(date, DEFAULT_SERVER_DATETIME_FORMAT) - timedelta(hours=2))
                    reason = reason_obj.search([('name', '=', reason_val)])
                    details = ''
                    if not reason:
                        reason = self.env.ref('mass_mailing_custom_unsubscribe.reason_other')
                        details = reason_val if reason_val else 'From Deregistration List'
                    if email:
                        contact_list = mail_list_obj.search([('email', '=', email)])
                        for contact in contact_list:
                            unsub_obj.create({
                                'date': date if date else now,
                                'mailing_list_ids': [(4, list.list_id.id) for list in contact.subscription_list_ids],
                                'email': email,
                                'action': 'unsubscription',
                                'reason_id': reason.id if reason else False,
                                'details': details,
                            })
                            for mail_list in contact.subscription_list_ids:
                                mail_list.opt_out = True
                        if not contact_list:
                            partners = partner_obj.search([('email', '=', email)])
                            for partner in partners:
                                unsub_obj.create({
                                    'date': date if date else now,
                                    'email': email,
                                    'action': 'unsubscription',
                                    'reason_id': reason.id if reason else '',
                                    'details': details,
                                    'unsubscriber_id': 'res.partner,' + str(partner.id)
                                })
                                black_list = black_list_obj.search([('email', '=', email)])
                                if not black_list:
                                    black_list_obj.create({'email': email})
        else:
            data = base64.decodestring(self.file)
            book = open_workbook(file_contents=data or b'')
            sheet = book.sheet_by_index(0)

            headers = []
            for rowx, row in enumerate(map(sheet.row, range(1)), 1):
                for colx, cell in enumerate(row, 1):
                    headers.append(cell.value)

            if headers != ['Email', 'Date', 'Reason']:
                raise UserError(_("Please correct Header in File!"))

            for rowx, row in enumerate(map(sheet.row, range(1, sheet.nrows)), 1):
                email = ''
                date = ''
                reason_val = ''
                for colx, cell in enumerate(row, 1):
                    if colx == 1:
                        email = cell.value
                    elif colx == 2:
                        date = cell.value
                    elif colx == 3:
                        reason_val = cell.value
                if date:
                    date = str(datetime.strptime(date, DEFAULT_SERVER_DATETIME_FORMAT) - timedelta(hours=2))
                if not isinstance(date, str):
                    raise UserError(_("Format Date column with String!"))
                reason = reason_obj.search([('name', '=', reason_val)])
                details = ''
                if not reason:
                    reason = self.env.ref('mass_mailing_custom_unsubscribe.reason_other')
                    details = reason_val if reason_val else 'From Deregistration List'
                if email:
                    contact_list = mail_list_obj.search([('email', '=', email)])
                    for contact in contact_list:
                        unsub_obj.create({
                            'date': date if date else now,
                            'mailing_list_ids': [(4, list.list_id.id) for list in contact.subscription_list_ids],
                            'email': email,
                            'action': 'unsubscription',
                            'reason_id': reason.id if reason else False,
                            'details': details,
                        })
                        for mail_list in contact.subscription_list_ids:
                            mail_list.opt_out = True
                    if not contact_list:
                        partners = partner_obj.search([('email', '=', email)])
                        for partner in partners:
                            unsub_obj.create({
                                'date': date if date else now,
                                'email': email,
                                'action': 'unsubscription',
                                'reason_id': reason.id if reason else '',
                                'details': details,
                                'unsubscriber_id': 'res.partner,' + str(partner.id)
                            })
                            black_list = black_list_obj.search([('email', '=', email)])
                            if not black_list:
                                black_list_obj.create({'email': email})
