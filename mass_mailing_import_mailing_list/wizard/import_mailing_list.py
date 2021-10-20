import base64
import csv
import io
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.modules.module import get_resource_path
import pytz
from xlrd import open_workbook

_logger = logging.getLogger(__name__)

class ImportMailingList(models.TransientModel):
    _name = 'import.mailing.list'

    file = fields.Binary(string='File')
    filename = fields.Char(string='File name')
    nr_total_rows = fields.Integer(string='Total number of rows')
    nr_imported_rows = fields.Integer(string='Successful rows')
    nr_failed_rows = fields.Integer(string='Failed rows')
    import_failed_mail_ids = fields.One2many(comodel_name='import.failed.mail', inverse_name='import_id')
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
            'activemail',
            'sökande id'
        ]
        if not all(item in header for item in correct_header):
            raise UserError(_('Please correct Header in file!\n'
                              'Header has to contain:\n') +
                            '\n'.join(correct_header))
        return header

    def get_contact(self, sokande_id, partner_obj, contact_obj):
        """Create mass_mailing_contact and tie it to res_partner"""
        # Search as sudo so that we search on res.partner
        partner = partner_obj.sudo().search([('customer_id', '=', sokande_id)])
        if not partner:
            return
        in_mail_unsubscription = self.env['mail.unsubscription'].search([('email', '=', partner.email)])
        if in_mail_unsubscription:
            return
        contact = contact_obj.search([('partner_id', '=', partner.id)])
        if contact:
            return contact.id
        contact = contact_obj.create({
            'partner_id': partner.id,
            'name': partner.name,
            'email': partner.email,
        })
        return contact.id

    def get_campaign(self):
        mailing_list = self.env['mail.mass_mailing.list'].search([('is_adkd_campaign', '=', True)])
        if not mailing_list:
            mailing_list = mailing_list.create(
                {
                    'name': _('ADKd Campaign'),
                    'is_adkd_campaign': True
                 })
        return mailing_list

    def get_mailing_list(self, active_mails):
        """
        Return mailing lists ids based on a set of ids from imported file.
        """
        mailing_list = self.env['mail.mass_mailing.list'].search([])
        mailing_list_ids = []
        for mail in active_mails:
            ml = mailing_list.filtered(lambda l: l.adkd_mail_name == mail)
            if not ml:
                ml = mailing_list.create({
                    'name': f'{mail} placeholder name',
                    'is_public': True,
                    'adkd_mail_name': mail,
                })
                ml.parent_id = self.get_campaign()
            mailing_list_ids.append(ml.id)
        return mailing_list_ids

    def insert_mail_contacts_to_mailing_lists(self,
                                              mailing_lists_ids,
                                              contacts,
                                              adkd_mail_list):
        """ Clears all contacts (not unsubscribed contacts) form the
            mailing lists and adds the imported contacts """
        mailing_lists = self.env['mail.mass_mailing.list'].browse(mailing_lists_ids)
        for mail_list in mailing_lists:
            # Get all opt out contacts ids for this list
            list_contact = self.env['mail.mass_mailing.list_contact_rel'].search([
                                                    ('list_id', '=', adkd_mail_list.id),
                                                    ('opt_out', '=', True)
                                                ]).contact_id.ids
            # Remove all contacts that did not opt out
            mail_list.write({
                'contact_ids': [(5,)]
                #'contact_ids': [(3, c.id) for c in mail_list.contact_ids if c.id not in list_contact]
            })
        list_contact = self.env['mail.mass_mailing.list_contact_rel']
        for mail_name, contact_id in contacts:
            mail_list = mailing_lists.filtered(
                lambda l: l.adkd_mail_name.upper() == mail_name)
            try:
                if mail_list:
                    list_contact_id = list_contact.search(
                            [('contact_id', '=', contact_id),
                             ('list_id', '=', adkd_mail_list.id)]
                        )
                    if list_contact_id and list_contact_id.opt_out:
                        continue
                    if not list_contact_id:
                        list_contact_id = list_contact.create(
                            {'contact_id': contact_id,
                             'list_id': adkd_mail_list.id}).id
                    mail_list.write({
                        'parent_id': adkd_mail_list.id,
                        'contact_ids': [(4, contact_id)],
                      #   'subscription_contact_ids': [(5, )],
                    })
                    c = self.env['mail.mass_mailing.contact'].browse(contact_id)
                    c.write({
                        'subscription_contact_ids': [(3, mail_list.id)],
                    })
            except Exception as e:
                print(e)
            else:
                _logger.warning('List not found')

    def import_data(self):
        """Parse and import a file."""
        if not self.file or not \
                self.filename.lower().endswith(
                    ('.xls', '.xlsx', '.csv', 'txt')):
            raise UserError(
                _("Please Select an .xls, .xlsx, .txt or .csv file to Import.")
            )
        partner_obj = self.env['res.partner']
        contact_obj = self.env['mail.mass_mailing.contact']
        failed_imports = []
        contacts = []
        active_mails = set()
        adkd_mail_list = False
        self.is_adkd_campaign = True
        if self.is_adkd_campaign:
            adkd_mail_list = self.get_campaign()
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
                    active_mail = row[headers['activemail']]
                    sokande_id = row[headers['sökande id']]
                except IndexError:
                    # Empty or malformed row.
                    _logger.warning(f'Could not parse the row: {row}')
                else:
                    # Add active_mail to set to get number of letters
                    active_mails.add(active_mail)
                    # Make list of tuples with (active_mail, contact_id)
                    contact = self.get_contact(sokande_id,
                                               partner_obj,
                                               contact_obj)
                    if contact:
                        contacts.append((active_mail.upper(), contact))
                    else:
                        failed_imports.append(
                            self.env['import.failed.mail'].create({
                                'sokande_id': sokande_id,
                                'active_mail': active_mail,
                            })
                        )

            mailing_lists = self.get_mailing_list(active_mails)
            self.insert_mail_contacts_to_mailing_lists(mailing_lists, contacts, adkd_mail_list)

        elif self.filename.lower().endswith(('.xls', '.xlsx')):
            data = base64.decodestring(self.file)
            book = open_workbook(file_contents=data or b'')
            sheet = book.sheet_by_index(0)

            # Verify Header, Force it lowercase and make a dict
            headers = self.check_header([cell.value for cell in sheet.row(0)])
            self.nr_total_rows = sheet.nrows
            for row_nr in range(1, sheet.nrows):
                active_mail = sheet.cell_value(row_nr, headers['activemail'])
                sokande_id = str(int(sheet.cell_value(row_nr, headers['sökande id'])))
                # Add active_mail to set to get number of letters
                active_mails.add(active_mail)
                # Make list of tuples with (active_mail, contact_id)
                contact = self.get_contact(sokande_id,
                                           partner_obj,
                                           contact_obj)
                if contact:
                    contacts.append((active_mail.upper(), contact))
                else:
                    failed_imports.append(
                        self.env['import.failed.mail'].create({
                            'sokande_id': sokande_id,
                            'active_mail': active_mail,
                        })
                    )
            mailing_lists = self.get_mailing_list(active_mails)
            self.insert_mail_contacts_to_mailing_lists(mailing_lists, contacts, adkd_mail_list)
        else:
            raise UserError(
                _('Unknown file ending: {}').format(self.filename)
            )
        self.nr_failed_rows = len(failed_imports)
        self.nr_imported_rows = self.nr_total_rows - self.nr_failed_rows
        self.import_failed_mail_ids = [(6,
                                        0,
                                        [f.id for f in failed_imports]
                                        )]
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



    def download_xls_file(self):
        xls_file_path = get_resource_path(
            'mass_mailing_autoresponder_crm_import',
            'static/file',
            'example_knime_import.xlsx')
        xls_file = False
        with open(xls_file_path, 'rb') as file_date:
            xls_file = base64.b64encode(file_date.read())
        if xls_file:
            self.dwnld_xls_filename = 'example_file.xlsx'
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
            self.dwnld_csv_filename = 'example_file.csv'
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
            self.dwnld_txt_filename = 'example_file.txt'
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


class ImportFailedMail(models.TransientModel):
    _name = 'import.failed.mail'

    import_id = fields.Many2one(comodel_name='import.mailing.list',
                                string="Rows that failed to be imported")
    sokande_id = fields.Char(string='Sökande id')
    active_mail = fields.Char(string='Active mail')
