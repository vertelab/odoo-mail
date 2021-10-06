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
from xlrd import open_workbook

_logger = logging.getLogger(__name__)


class ImportKnimeExportWizard(models.TransientModel):
    _name = 'import.knime.export.wizard'
    _description = 'Import Knime Export'

    file = fields.Binary(string='File')
    filename = fields.Char(string='File name')
    # segment = fields.Char()
    # active_mail = fields.Char()
    # send_today = fields.Boolean()
    nr_total_rows = fields.Integer(string='Total number of rows')
    nr_imported_rows = fields.Integer(string='Successful rows')
    nr_failed_rows = fields.Integer(string='Failed rows')
    import_failed_knime_ids = fields.One2many(comodel_name='import.failed.knime', inverse_name='import_id')
    has_failed_imports = fields.Boolean()
    is_imported = fields.Boolean()
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
        correct_header = [
            'e-postadress',
            'segment',
            'sendtoday',
            'activemail',
            'sökande id'
        ]
        if not all(item in header for item in correct_header):
            raise UserError(_('Please correct Header in file!\n'
                              'Header has to contain:\n') +
                            '\n'.join(correct_header))
        return header


    def import_row(self, segment, send_today,
                   active_mail, sokande_id, partner_obj, campaign_obj):
        """Handle an individual row."""
        # Search as sudo so that we search on res.partner
        partner = partner_obj.sudo().search([('customer_id', '=', sokande_id)])
        if not partner or segment not in ('a', 'b', 'c'):
            self.has_failed_imports = True
            # Return vals of row that was not imported for user feedback
            send_today = True if send_today.lower() == 'j' else False
            return {
                'sokande_id': sokande_id,
                'active_mail': active_mail,
                'segment_jobseeker': segment,
                'send_today': send_today
            }
        partner.segment_jobseeker = segment

        if not partner.mail_adkd_campaign_ids.filtered(
                lambda l: l.name == active_mail):
            # Check if there is already a campaign with this name
            campaign = campaign_obj.search([('name', '=', active_email)])
            if not campaign:
                campaign = campaign_obj.create({'name': active_mail})
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
        failed_imports = []
        if self.filename.lower().endswith(('.csv', '.txt')):
            # Decode data to string, Odoo supplies it as base64
            csv_data = base64.b64decode(self.file)
            try:
                data_file = io.StringIO(csv_data.decode("ISO-8859-1"))
            except Exception as e:
                raise UserError('Error %s' % e)
            # Read CSV
            headers, *data = csv.reader(data_file, delimiter=';')

            # Verify Header, Force it lowercase and make a dict
            headers = self.check_header(headers)
            self.nr_total_rows = len(data)
            for row in data:
                try:
                    segment = row[headers['segment']].lower().strip()
                    send_today = row[headers['sendtoday']]
                    active_mail = row[headers['activemail']]
                    sokande_id = row[headers['sökande id']]
                except IndexError:
                    # Empty or malformed row.
                    _logger.warning(f'Could not parse the row: {row}')
                else:
                    failed_import = self.import_row(
                            segment, send_today,
                            active_mail, sokande_id,
                            partner_obj, campaign_obj)
                    if failed_import:
                        failed_imports.append(failed_import)
        elif self.filename.lower().endswith(('.xls', '.xlsx')):
            data = base64.decodestring(self.file)
            book = open_workbook(file_contents=data or b'')
            sheet = book.sheet_by_index(0)

            # Verify Header, Force it lowercase and make a dict
            headers = self.check_header([cell.value for cell in sheet.row(0)])
            self.nr_total_rows = sheet.nrows
            for row_nr in range(1, sheet.nrows):
                segment = sheet.cell_value(row_nr,
                                           headers['segment']).lower().strip()
                send_today = sheet.cell_value(row_nr, headers['sendtoday'])
                active_mail = sheet.cell_value(row_nr, headers['activemail'])
                sokande_id = sheet.cell_value(row_nr, headers['sökande id'])
                self.import_row(segment, send_today,
                                active_mail, sokande_id,
                                partner_obj, campaign_obj)
        else:
            raise UserError(
                _('Unknown file ending: {}').format(self.filename))
        self.nr_failed_rows = len(failed_imports)
        self.nr_imported_rows = self.nr_total_rows - self.nr_failed_rows
        self.is_imported = True
        if self.has_failed_imports:
            ids = []
            for failed in failed_imports:
                ids.append(self.env['import.failed.knime'].create(failed).id)
            self.import_failed_knime_ids = [(6, 0, [])]
            self.import_failed_knime_ids = [(6, 0, ids)]
            return {
                'name': _('Some rows failed to be imported'),
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'import.knime.export.wizard',
                'res_id': self.id,
                'type': 'ir.actions.act_window',
                'target': 'new',
            }



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

class ImportFailedKnime(models.TransientModel):
    _name = 'import.failed.knime'

    import_id = fields.Many2one(comodel_name='import.knime.export.wizard',
                                string="Rows that failed to be imported")
    sokande_id = fields.Char(string='Sökande id')
    send_today = fields.Boolean(string='Send today')
    active_mail = fields.Char(string='Active mail')
    segment_jobseeker = fields.Char(string='Segment')
