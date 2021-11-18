import base64
import csv
import io
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.modules.module import get_resource_path
from xlrd import open_workbook

_logger = logging.getLogger(__name__)

class ImportMailingList(models.TransientModel):
    """
    Import knime mailing list.
    If 'ADKd campaign' is selected we will create
    a parent mailing list for all the imported mailing lists.
    We do this in order to be able to unsubscribe to all the
    ADKd campaign new letters from the imported file. If a
    customer unsubscribes to ADKd Campaign list then the customer
    will not be imported to any of the children list next time.
    """
    _name = 'import.mailing.list'

    file = fields.Binary(string='File')
    filename = fields.Char(string='File name')
    nr_total_rows = fields.Integer(string='Total number of rows')
    nr_imported_rows = fields.Integer(string='Successful rows')
    nr_failed_rows = fields.Integer(string='Failed rows')
    import_failed_mail_ids = fields.One2many(
                                    comodel_name='import.failed.mail',
                                    inverse_name='import_id')
    list_name = fields.Char(string='Mailing list name')
    is_imported = fields.Boolean()
    import_type = fields.Selection(
        string="Import type",
        selection=[("adkd", "ADKd Campaign"),
                   ("micro", "Micro campaigns")],
    )
    file = fields.Binary(string='File')
    filename = fields.Char(string='File name')
    example_filename = fields.Char("File name")
    example_file = fields.Binary("File")


    @staticmethod
    def check_header(header, import_type):
        """
        Verify that header has the required columns as well as create
         a dict with indexes.
         """
        # Verify Header, Force it lowercase
        header = {x.lower(): index for index, x in enumerate(header)}
        correct_header = []
        if import_type == 'adkd':
            correct_header = [
                'activemail' or '',
                'sökande id'
            ]
        elif import_type:
            correct_header = ['sökande id']
        if not all(item in header for item in correct_header):
            raise UserError(_('Please correct Header in file!\n'
                              'Header has to contain:\n') +
                            '\n'.join(correct_header))
        return header

    def _get_contact(self, sokande_id, partner_obj, contact_obj, email):
        """Create mass_mailing_contact and tie it to res_partner"""
        # Need to do sudo here if res_partner.is_jobseeker is True
        partner = partner_obj.sudo().search(
            [('customer_id', '=', sokande_id)]
        )
        if not partner:
            return
        # Check for blacklist
        if self.env['mail.unsubscription'].search(
                [('email', '=', partner.email)]
        ):
            return
        contact = contact_obj.search([('partner_id', '=', partner.id)])
        if contact:
            return contact.id
        contact = contact_obj.create({
            'partner_id': partner.id,
            'name': partner.name,
            # If partner doesn't have email then use imported email
            'email': partner.email or email,
        })
        return contact.id

    def get_campaign(self, campaign):
        mailing_list = False
        if campaign == 'adkd':
            mailing_list = self.env['mail.mass_mailing.list'].search(
                [('list_type', '=', 'adkd'), ('parent_id', '=', False)]
            )
            if not mailing_list:
                mailing_list = mailing_list.create(
                    {
                        'name': _('ADKd Campaign'),
                        'list_type': 'ADKd',
                     })
            elif len(mailing_list) > 1:
                raise UserError(
                    _('There already exist a ADKd Campaign mailing list '
                      f'"{mailing_list.name}". There can be only one at a time.')
                )
        elif campaign == 'micro':
            mailing_list = self.env['mail.mass_mailing.list'].search(
                [('list_type', '=', 'Micro Campaign'), ('parent_id', '=', False)]
            )
            if not mailing_list:
                mailing_list = mailing_list.create(
                    {
                        'name': _('Micro Campaign'),
                        'list_type': _('Micro Campaign'),
                    })
            elif len(mailing_list) > 1:
                raise UserError(
                    _('There already exist a Micro Campaign mailing list '
                      f'"{mailing_list.name}". There can be only one at a time.')
                )
        return mailing_list

    def get_mailing_list(self, active_mails):
        """
        Return mailing lists ids based on a set of
        ids from imported file.
        """
        campaign_id = self.get_campaign(self.import_type)
        if self.import_type == 'adkd':
            mailing_list = self.env['mail.mass_mailing.list'].search([])
            mailing_list_ids = []
            for mail in active_mails:
                ml = mailing_list.filtered(lambda l: l.adkd_mail_name == mail)
                if not ml:
                    ml = mailing_list.create({
                        'name': f'{mail} placeholder name',
                        'is_public': True,
                        'adkd_mail_name': mail,
                        'list_type': 'ADKd'
                    })
                    ml.parent_id = campaign_id
                mailing_list_ids.append(ml.id)
            return mailing_list_ids
        elif self.import_type == 'micro':
            mailing_list = self.env['mail.mass_mailing.list'].search([('adkd_mail_name', '=', self.list_name)])
            if not mailing_list:
                mailing_list = mailing_list.create({
                    'name': self.list_name,
                    'is_public': True,
                    'adkd_mail_name': self.list_name,
                    'list_type': _('Micro Campaign'),
                })
                mailing_list.parent_id = campaign_id
            return mailing_list.id


    def insert_mail_contacts_to_mailing_lists(self,
                                              mailing_lists_ids,
                                              contacts):
        """
        Clears all contacts form the
        mailing lists and adds the imported contacts
        unless they have opted out for adkd campaign
        """
        mailing_lists = self.env['mail.mass_mailing.list'].browse(
            mailing_lists_ids
        )
        for mail_list in mailing_lists:
            mail_list.write({
                'contact_ids': [(5, )]
            })
        list_contact = self.env['mail.mass_mailing.list_contact_rel']
        for mail_name, contact_id in contacts:
            mail_list = False
            if self.import_type == 'adkd':
                mail_list = mailing_lists.filtered(
                    lambda l: l.adkd_mail_name.upper() == mail_name)
            elif self.import_type == 'micro':
                mail_list = mailing_lists[0]
            if mail_list:
                list_contact_id = list_contact.search(
                        [('contact_id', '=', contact_id),
                         ('list_id', '=', mail_list.parent_id.id)]
                    )
                if list_contact_id and list_contact_id.opt_out:
                    continue
                mail_list.write({
                    'contact_ids': [(4, contact_id)],
                })
                # Write the same ids to parent campaign
                mail_list.parent_id.write({
                    'contact_ids': [(4, contact_id)],
                })

    def import_data(self):
        """Parse and import a file."""
        if not self.file:
            raise UserError(_('You must upload a file to import'))
        if self.import_type == 'micro' and not self.list_name:
            raise UserError(_('You must specify a name for mailing list'))
        if self.filename.lower().endswith(('.csv', '.txt')):
            try:
                self.parse_csv_data()
            except UnicodeDecodeError as e:
                print(e)
        elif self.filename.lower().endswith(('.xls', '.xlsx')):
            self.parse_xlsx_data()
        else:
            raise UserError(
                _("Please Select an .xls, .xlsx, "
                  ".txt or .csv file to Import.")
            )
        self.nr_failed_rows = len(self.import_failed_mail_ids)
        self.nr_imported_rows = self.nr_total_rows - self.nr_failed_rows
        self.is_imported = True
        return {
            'name': _('Imported rows'),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'import.mailing.list',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def parse_csv_data(self):
        # Decode data to string, Odoo supplies it as base64
        csv_data = base64.b64decode(self.file)
        try:
            data_file = io.StringIO(csv_data.decode("ISO-8859-1"))
        except UnicodeDecodeError as e:
            raise UserError(f'Error {e}')
        # Read CSV
        headers, *data = csv.reader(data_file, delimiter=';')
        if len(data) == 0:
            raise UserError(f'File is empty')
        # Verify Header, Force it lowercase and make a dict
        headers = self.check_header(headers, self.import_type)
        partner_obj = self.env['res.partner']
        contact_obj = self.env['mail.mass_mailing.contact']
        contacts = []
        active_mails = set()
        self.nr_total_rows = len(data)
        for row in data:
            try:
                active_mail = ''
                if self.import_type == 'adkd':
                    active_mail = row[headers['activemail']]
                sokande_id = row[headers['sökande id']]
                if 'e-postadress' in headers:
                    email = row[headers['e-postadress']]
                else:
                    email = ''
            except IndexError:
                # Empty or malformed row.
                msg = _('Could not parse the row: {row}').format(row=row)
                _logger.warning(msg)
                raise UserError(msg)
            else:
                contact = self._get_contact(sokande_id,
                                            partner_obj,
                                            contact_obj,
                                            email)
                if contact:
                    # Make list of tuples with (active_mail, contact_id)
                    contacts.append((active_mail.upper(), contact))
                    # Add active_mail to set to get number of letters
                    active_mails.add(active_mail)
                else:
                    failed_import_id = self.env['import.failed.mail'].create({
                        'sokande_id': sokande_id,
                        'active_mail': active_mail,
                    }).id
                    self.write({
                        'import_failed_mail_ids': [(4, failed_import_id)]
                    })

        mailing_lists = self.get_mailing_list(active_mails)
        self.insert_mail_contacts_to_mailing_lists(mailing_lists,
                                                   contacts)

    def parse_xlsx_data(self):
        data = base64.decodestring(self.file)
        book = open_workbook(file_contents=data or b'')
        sheet = book.sheet_by_index(0)
        partner_obj = self.env['res.partner']
        contact_obj = self.env['mail.mass_mailing.contact']
        contacts = []
        active_mails = set()
        if sheet.nrows == 0:
            raise UserError(f'File is empty')
        # Verify Header, Force it lowercase and make a dict
        headers = self.check_header([cell.value for cell in sheet.row(0)], self.import_type)
        self.nr_total_rows = sheet.nrows - 1
        for row_nr in range(1, sheet.nrows):
            active_mail = ''
            if self.import_type == 'adkd':
                active_mail = sheet.cell_value(row_nr, headers['activemail'])
            sokande_id = str(int(sheet.cell_value(row_nr,
                                                  headers['sökande id'])))
            if 'e-postadress' in headers:
                email = sheet.cell_value(row_nr,
                                         headers['e-postadress'])
            else:
                email = ''
            # Add active_mail to set to get number of letters
            active_mails.add(active_mail)
            # Make list of tuples with (active_mail, contact_id)
            contact = self._get_contact(sokande_id,
                                        partner_obj,
                                        contact_obj,
                                        email)
            if contact:
                contacts.append((active_mail.upper(), contact))
            else:
                failed_import_id = self.env['import.failed.mail'].create({
                    'sokande_id': sokande_id,
                    'active_mail': active_mail,
                }).id
                self.write({
                    'import_failed_mail_ids': [(4, failed_import_id)]
                })
        mailing_lists = self.get_mailing_list(active_mails)
        self.insert_mail_contacts_to_mailing_lists(mailing_lists,
                                                   contacts)

    def download_file(self):
        # Get file type from context
        file_type = self._context.get('file_type')
        if file_type == 'csv':
            file_extension = '.csv'
        elif file_type == 'txt':
            file_extension = '.txt'
        elif file_type == 'xlsx':
            file_extension = '.xlsx'
        file_path = get_resource_path(
            'mass_mailing_import_mailing_list',
            'static/file',
            f'example_file{file_extension}')
        file = False
        with open(file_path, 'rb') as file_date:
            file = base64.b64encode(file_date.read())
        if file:
            self.example_filename = f'example_file{file_extension}'
            self.example_file = file
        return {
            'name': 'Import',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'import.mailing.list',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id,
        }


class ImportFailedMail(models.TransientModel):
    """
    This is used for feedback on the imported file for the user.
    It will show the user
        Total imported rows
        Failed rows
        Successful rows
        Sokande id for failed row
        Active mail
    """
    _name = 'import.failed.mail'

    import_id = fields.Many2one(comodel_name='import.mailing.list',
                                string="Rows that failed to be imported")
    sokande_id = fields.Char(string='Sökande id')
    active_mail = fields.Char(string='Active mail')
