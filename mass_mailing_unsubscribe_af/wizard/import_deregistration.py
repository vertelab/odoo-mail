import base64
import csv
import io
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from xlrd import open_workbook
from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.modules.module import get_resource_path

class ImportDeregistratioFile(models.TransientModel):
    _name = 'import.deregistration.file'
    _description = 'Import Deregistration File'

    file = fields.Binary(string='File')
    filename = fields.Char(string='File name')
    dwnld_csv_filename = fields.Char("CSV File name")
    dwnld_xls_filename = fields.Char("XLS File name")
    dwnld_txt_filename = fields.Char("TXT File name")
    dwnld_csv_file = fields.Binary("CSV File")
    dwnld_xls_file = fields.Binary("XLS File")
    dwnld_txt_file = fields.Binary("TXT File")

    def import_data(self):
        if not self.file or not \
                self.filename.lower().endswith(('.xls', '.xlsx', '.csv', 'txt')):
            raise UserError(_("Please Select an .xls, .xlsx, .txt or .csv file to Import."))
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
            correct_header = ['E-postadress', 'Opt out date', 'Reason']
            check_header = all(item in headers for item in correct_header)
            if not check_header:
                raise UserError(_("Please correct Header in file!"))
            else:
                for row in result_vals:
                    email = row.get('E-postadress')
                    date = row.get('Opt out date')
                    reason_val = row.get('Reason')
                    if date:
                        date = str(datetime.strptime(str(date), '%Y-%m-%d %H:%M') - timedelta(hours=2))
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
        elif self.filename.lower().endswith('.txt'):
            file_data = base64.decodestring(self.file)
            file_data = file_data.decode("utf-8")
            data_list = file_data.split('\n')
            for data in data_list[1:]:
                if data:
                    row = data.split(',')
                    if len(row) < 3:
                        raise UserError(_("Correct following line! \n %s" % row))
                    else:
                        email = row[1]
                        date = row[2]
                        reason_val = row[3]
                        if date:
                            date = str(datetime.strptime(str(date), '%Y-%m-%d %H:%M') - timedelta(hours=2))
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
        else:
            data = base64.decodestring(self.file)
            book = open_workbook(file_contents=data or b'')
            sheet = book.sheet_by_index(0)

            headers = []
            for rowx, row in enumerate(map(sheet.row, range(1)), 1):
                for colx, cell in enumerate(row, 1):
                    headers.append(cell.value)

            correct_header = ['E-postadress', 'Opt out date', 'Reason']
            check_header = all(item in headers for item in correct_header)
            if not check_header or (len(headers) < 3) or (headers[1] != 'E-postadress') or \
                    (headers[2]!= 'Opt out date') or (headers[3] != 'Reason'):
                raise UserError(_("Please correct Header in File!"))

            for rowx, row in enumerate(map(sheet.row, range(1, sheet.nrows)), 1):
                email = ''
                date = ''
                reason_val = ''
                for colx, cell in enumerate(row, 1):
                    if colx == 2:
                        email = cell.value
                    elif colx == 3:
                        date = cell.value
                    elif colx == 4:
                        reason_val = cell.value
                if date:
                    date = str(datetime.strptime(str(date), '%Y-%m-%d %H:%M') - timedelta(hours=2))
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

    def download_xls_file(self):
        xls_file_path = get_resource_path(
            'mass_mailing_unsubscribe_af', 'static/file', 'Optout_Apsis.xlsx')
        xls_file = False
        with open(xls_file_path, 'rb') as file_date:
            xls_file = base64.b64encode(file_date.read())
        if xls_file:
            self.dwnld_xls_filename = 'Optout_Apsis.xlsx'
            self.dwnld_xls_file = xls_file
        return {
            'name': 'Deregistration',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'import.deregistration.file',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id,
        }

    def download_csv_file(self):
        csv_file_path = get_resource_path(
            'mass_mailing_unsubscribe_af', 'static/file', 'Optout_Apsis.csv')
        csv_file = False
        with open(csv_file_path, 'rb') as file_date:
            csv_file = base64.b64encode(file_date.read())
        if csv_file:
            self.dwnld_csv_filename = 'Optout_Apsis.csv'
            self.dwnld_csv_file = csv_file
        return {
            'name': 'Deregistration',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'import.deregistration.file',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id,
        }

    def download_txt_file(self):
        txt_file_path = get_resource_path(
            'mass_mailing_unsubscribe_af', 'static/file', 'Optout_Apsis.txt')
        txt_file = False
        with open(txt_file_path, 'rb') as file_date:
            txt_file = base64.b64encode(file_date.read())
        if txt_file:
            self.dwnld_txt_filename = 'Optout_Apsis.txt'
            self.dwnld_txt_file = txt_file
        return {
            'name': 'Deregistration',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'import.deregistration.file',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id,
        }

