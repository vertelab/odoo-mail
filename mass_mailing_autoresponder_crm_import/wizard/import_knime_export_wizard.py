import base64
from datetime import datetime, timedelta
import csv
import io
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.modules.module import get_resource_path
import pytz
from xlrd import open_workbook

_logger = logging.getLogger(__name__)


class ImportKnimeExportWizard(models.TransientModel):
    _name = 'import.knime.export.wizard'
    _description = 'Import Knime Export'

    file = fields.Binary(string='File')
    filename = fields.Char(string='File name')
    segment = fields.Char()
    email = fields.Char()
    active_mail = fields.Char()
    send_today = fields.Boolean()

    file = fields.Binary(string='File')
    filename = fields.Char(string='File name')
    dwnld_csv_filename = fields.Char("CSV File name")
    dwnld_xls_filename = fields.Char("XLS File name")
    dwnld_txt_filename = fields.Char("TXT File name")
    dwnld_csv_file = fields.Binary("CSV File")
    dwnld_xls_file = fields.Binary("XLS File")
    dwnld_txt_file = fields.Binary("TXT File")


    @staticmethod
    def check_header(header):
        """
        Verify that header has the required columns as well as create
         a dict with indexes.
         """
        # Verify Header, Force it lowercase
        header = {x.lower(): index for index, x in enumerate(header)}
        correct_header = ['e-postadress', 'segment', 'sendtoday', 'activemail']
        if not all(item in header for item in correct_header):
            raise UserError(_('Please correct Header in file!\n'
                              'Header has to contain:\n') +
                            '\n'.join(correct_header))
        return header


    def import_row(self, email, segment, send_today,
                   active_email, partner_obj, campaign_obj):
        """Handle an individual row."""
        partner = partner_obj.search([('email', '=', email)], limit=1)
        if not partner:
            raise UserError(
                _('Can not find jobseeker with email: {}').format(email))
        if segment == 'a' or segment == 'b' or segment == 'c':
            partner.segment_jobseeker = segment
        else:
            raise UserError(_('Invalid segment. Segment should be A, B or C'))
        campaign = campaign_obj.search(
            [('name', 'ilike', active_email)],
            limit=1)
        if len(campaign) == 1:
            partner.mail_adkd_campaign_ids = [(4, campaign.id)]
        else:
            campaign = campaign_obj.create({'name': active_email})
            partner.mail_adkd_campaign_ids = [(4, campaign.id)]


    def import_data(self):
        """Parse and import a file."""
        if not self.file or not \
                self.filename.lower().endswith(
                    ('.xls', '.xlsx', '.csv', 'txt')):
            raise UserError(
                _("Please Select an .xls, .xlsx, .txt or .csv file to Import.")
            )
        partner_obj = self.env['res.partner']
        campaign_obj = self.env['res.partner.mail.adkd.campaign']

        if self.filename.lower().endswith(('.csv', '.txt')):
            # Decode data to string, Odoo supplies it as base64
            csv_data = base64.b64decode(self.file)
            data_file = io.StringIO(csv_data.decode("utf-8"))
            # Read CSV
            headers, *data = csv.reader(data_file, delimiter=';')

            # Verify Header, Force it lowercase and make a dict
            headers = self.check_header(headers)
            for row in data:
                try:
                    email = row[headers['e-postadress']]
                    segment = row[headers['segment']].lower().strip()
                    send_today = row[headers['sendtoday']]
                    active_mail = row[headers['activemail']]
                except IndexError:
                    # Empty or malformed row.
                    _logger.warning(f'Could not parse the row: {row}')
                else:
                    self.import_row(email, segment, send_today,
                                    active_mail, partner_obj, campaign_obj)

        elif self.filename.lower().endswith(('.xls', '.xlsx')):
            data = base64.decodestring(self.file)
            book = open_workbook(file_contents=data or b'')
            sheet = book.sheet_by_index(0)

            # Verify Header, Force it lowercase and make a dict
            headers = self.check_header([cell.value for cell in sheet.row(0)])
            for row_nr in range(sheet.nrows, 1):
                email = sheet.cell_value(row_nr, headers['e-postadress'])
                segment = sheet.cell_value(row_nr,
                                           headers['segment'].lower().strip())
                send_today = sheet.cell_value(row_nr, headers['sendToday'])
                active_mail = sheet.cell_value(row_nr, headers['activeMail'])
                self.import_row(email, segment, send_today,
                                active_mail, partner_obj, campaign_obj)
        else:
            raise UserError(_('Unknown file ending: {}').format(self.filename))


    def download_xls_file(self):
        xls_file_path = get_resource_path(
            'mass_mailing_autoresponder_crm_import',
            'static/file',
            'example_knime_import.xlsx')
        xls_file = False
        with open(xls_file_path, 'rb') as file_date:
            xls_file = base64.b64encode(file_date.read())
        if xls_file:
            self.dwnld_xls_filename = 'example_knime_import.xlsx'
            self.dwnld_xls_file = xls_file
        return {
            'name': 'Import',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'import.knime.export.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id,
        }

    def download_csv_file(self):
        csv_file_path = get_resource_path(
            'mass_mailing_autoresponder_crm_import',
            'static/file',
            'example_knime_import.csv')
        csv_file = False
        with open(csv_file_path, 'rb') as file_date:
            csv_file = base64.b64encode(file_date.read())
        if csv_file:
            self.dwnld_csv_filename = 'example_knime_import.csv'
            self.dwnld_csv_file = csv_file
        return {
            'name': 'Import',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'import.knime.export.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id,
        }

    def download_txt_file(self):
        txt_file_path = get_resource_path(
            'mass_mailing_autoresponder_crm_import',
            'static/file',
            'example_knime_import.txt')
        txt_file = False
        with open(txt_file_path, 'rb') as file_date:
            txt_file = base64.b64encode(file_date.read())
        if txt_file:
            self.dwnld_txt_filename = 'example_knime_import.txt'
            self.dwnld_txt_file = txt_file
        return {
            'name': 'Import',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'import.knime.export.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id,
        }
