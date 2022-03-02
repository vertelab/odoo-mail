import datetime
import logging

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


def create_mass_mailing(env, mailing_model='res.partner'):
    source = env['utm.source'].create({'name': 'TEST'})
    vals = {'email_from': 'TEST',
            'keep_archives': False,
            'mailing_model_real': mailing_model,
            'name': 'TEST',
            'reply_to_mode': 'email',
            'source_id': source.id,
            'state': 'done'}
    return env['mail.mass_mailing'].create(vals)


def create_mass_mailing_statistics(env, mass_mailing, num=1):
    vals = {'mass_mailing_id': mass_mailing.id,
            'sent': datetime.datetime.now(),
            'opened': datetime.datetime.now(),
            }
    return env['mail.mail.statistics'].create([vals for x in range(num)])


@tagged("post_install", "-at_install", "mass_mailing", "mass_mailing_statistics_af")
class MassMailingStatisticsTest(TransactionCase):

    def test_basic_calculations(self):
        """Test basic functionality and fields with default settings."""
        mass_mailing = create_mass_mailing(self.env)
        create_mass_mailing_statistics(self.env, mass_mailing, 3)
        for field, expected in (('sent', '3'),
                                ('opened', '3'),
                                ('received', '3'),
                                ('ignored', 0),
                                ('bounced', '0'),
                                ('failed', 0),
                                ('scheduled', 0),
                                ('clicks', '0'),
                                ('total_clicks', 0),
                                ('replied', 0)):
            with self.subTest(field=field):
                self.assertEqual(getattr(mass_mailing, field), expected)

    def test_scheduled(self):
        """Test that a scheduled mailing gets counted correctly."""
        mass_mailing = create_mass_mailing(self.env)
        statistics = create_mass_mailing_statistics(self.env, mass_mailing, 3)
        statistics[2].sent = False
        self.assertEqual(mass_mailing.scheduled, 1)

    def test_ignored(self):
        """Test that ignored mails get counted correctly."""
        mass_mailing = create_mass_mailing(self.env)
        statistics = create_mass_mailing_statistics(self.env, mass_mailing, 3)
        statistics[2].sent = False
        statistics[2].ignored = datetime.datetime.now()
        self.assertEqual(mass_mailing.ignored, 1)

    def test_clicks(self):
        """
        Test that clicks, total_clicks, clics_ratio
        and ctor gets calculated correctly.
        """
        mass_mailing = create_mass_mailing(self.env)
        statistics = create_mass_mailing_statistics(self.env, mass_mailing, 3)
        statistics[0].opened = False
        statistics[2].clicked = datetime.datetime.now()
        statistics[2].total_clicks = 1
        statistics[1].clicked = datetime.datetime.now()
        statistics[1].total_clicks = 2

        self.assertEqual(mass_mailing.clicks, '2')
        self.assertEqual(mass_mailing.total_clicks, 3)
        self.assertEqual(mass_mailing.clicks_ratio, 66)
        self.assertEqual(mass_mailing.ctor, 100)

    def test_replied(self):
        """Check that replied gets calculated correctly."""
        mass_mailing = create_mass_mailing(self.env)
        statistics = create_mass_mailing_statistics(self.env, mass_mailing, 3)
        statistics[2].replied = datetime.datetime.now()
        self.assertEqual(mass_mailing.replied, 1)

    def test_bounced(self):
        """Test that bounced gets calculated correctly."""
        mass_mailing = create_mass_mailing(self.env)
        statistics = create_mass_mailing_statistics(self.env, mass_mailing, 3)
        statistics[2].bounced = datetime.datetime.now()
        self.assertEqual(mass_mailing.bounced, '1')

    def test_failed(self):
        """Test that failed is calculated correctly."""
        mass_mailing = create_mass_mailing(self.env)
        statistics = create_mass_mailing_statistics(self.env, mass_mailing, 3)
        statistics[2].bounced = datetime.datetime.now()
        self.assertEqual(mass_mailing.bounced, '1')
