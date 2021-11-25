import base64
import csv
from datetime import datetime, timedelta
import io
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.modules.module import get_resource_path
import pytz
from xlrd import open_workbook, xldate_as_tuple

_logger = logging.getLogger(__name__)


class ImportDeregistrationFile(models.TransientModel):
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

    @staticmethod
    def adjust_tz(date, from_tz='Europe/Stockholm', to_tz='utc'):
        """Change between timezones."""
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d %H:%M')
        elif isinstance(date, tuple):
            date = datetime(*date[:6])
        to_tz = pytz.timezone(to_tz)
        return pytz.timezone(from_tz).localize(date).astimezone(to_tz).replace(tzinfo=None)

    @staticmethod
    def check_header(header):
        """
        Verify that header has the required columns as well as create
         a dict with indexes.
         """
        # Verify Header, Force it lowercase
        header = {x.lower(): index for index, x in enumerate(header)}
        correct_header = ['opt out date', 'reason', 'sokande_id']
        if not all(item in header for item in correct_header):
            raise UserError(_('Please correct Header in file!\n'
                              'Header has to contain:\n') +
                            '\n'.join(correct_header))
        return header

    def import_row(self, date, reason_val, unsub_obj, mail_list_obj,
                   black_list_obj, partner_obj, reason_obj, sokande_id):
        """Handle an individual row."""
        date = self.adjust_tz(date)
        reason = reason_obj.search([('name', '=', reason_val)])
        details = ''
        if not reason:
            reason = self.env.ref('mass_mailing_custom_unsubscribe.reason_other')
            details = reason_val if reason_val else 'From Deregistration List'
        if sokande_id:
            partner_id = partner_obj.sudo().search([
                ('customer_id', '=', sokande_id)
            ])
            contact = mail_list_obj.search([('partner_id', '=', partner_id.id)])
            if contact:
                unsub_obj.create({
                        'date': date,
                        'mailing_list_ids':
                            [(4, lst.list_id.id) for lst in
                             contact.subscription_list_ids],
                        'email': partner_id.email,
                        'action': 'unsubscription',
                        'reason_id': reason.id if reason else '',
                        'details': details,
                })
                if not black_list_obj.search([
                    ('email', '=', partner_id.email)
                ]):
                    black_list_obj.create({'email': partner_id.email})
                for mail_list in contact.subscription_list_ids:
                    mail_list.opt_out = True
            else:
                unsub_obj.create({
                        'date': date,
                        'email': partner_id.email,
                        'action': 'unsubscription',
                        'reason_id': reason.id if reason else '',
                        'details': details,
                        'unsubscriber_id': 'res.partner,' + str(partner_id.id)
                })
                if not black_list_obj.search([
                    ('email', '=', partner_id.email)
                ]):
                    black_list_obj.create({'email': partner_id.email})


    def import_data(self):
        """Parse and import a file."""
        if not self.file or not \
                self.filename.lower().endswith(('.xls', '.xlsx', '.csv', 'txt')):
            raise UserError(_("Please Select an .xls, .xlsx, .txt or .csv file to Import."))
        unsub_obj = self.env['mail.unsubscription']
        mail_list_obj = self.env['mail.mass_mailing.contact']
        black_list_obj = self.env['mail.blacklist']
        partner_obj = self.env['res.partner']
        reason_obj = self.env['mail.unsubscription.reason']
        now = datetime.now()
        if self.filename.lower().endswith(('.csv', '.txt')):
            # Decode data to string, Odoo supplies it as base64
            csv_data = base64.b64decode(self.file)
            data_file = io.StringIO(csv_data.decode("utf-8"))
            # Read CSV
            headers, *data = csv.reader(data_file, delimiter=',')

            # Verify Header, Force it lowercase and make a dict
            headers = self.check_header(headers)
            for row in data:
                try:
                    sokande_id = row[headers['sokande_id']]
                    date = row[headers['opt out date']] or now
                    reason_val = row[headers['reason']]
                except IndexError:
                    # Empty or malformed row.
                    _logger.warning(f'Could not parse the row: {row}')
                else:
                    self.import_row(date, reason_val, unsub_obj,
                                    mail_list_obj,black_list_obj, partner_obj,
                                    reason_obj, sokande_id)

        elif self.filename.lower().endswith(('.xls', '.xlsx')):
            data = base64.decodestring(self.file)
            book = open_workbook(file_contents=data or b'')
            sheet = book.sheet_by_index(0)

            # Verify Header, Force it lowercase and make a dict
            headers = self.check_header([cell.value for cell in sheet.row(0)])
            for row_nr in range(1, sheet.nrows):
                sokande_id = sheet.cell_value(row_nr, headers['sokande_id'])
                if isinstance(sokande_id, (float, int)):
                    sokande_id = int(sokande_id)
                else:
                    raise UserError(
                        _("Sökande ID has to be an integer!"
                          " Imported value was: {sokande_id}").format(
                            **locals()
                        )
                    )
                date = sheet.cell_value(row_nr, headers['opt out date'])
                # Excel can store a date in different ways, handle two common ones.
                if isinstance(date, str):
                    date = datetime.strptime(date, '%Y-%m-%d %H:%M')
                elif isinstance(date, float):
                    date = xldate_as_tuple(date, book.datemode)
                else:
                    raise UserError(f'Unsupported date format: {date} of the type {type(date)}')
                reason_val = sheet.cell_value(row_nr, headers['reason'])
                self.import_row(date, reason_val, unsub_obj,
                                mail_list_obj, black_list_obj, partner_obj,
                                reason_obj, sokande_id)
        else:
            raise UserError(_('Unknown file ending: {}').format(self.filename))

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
