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
        self.assertEqual(mass_mailing.sent, '2')

    def test_clicks(self):
        """
        Test that clicks, total_clicks, clicks_ratio
        and ctor gets calculated correctly.
        """
        mass_mailing = create_mass_mailing(self.env)
        statistics = create_mass_mailing_statistics(self.env, mass_mailing, 3)
        statistics[0].opened = False
        statistics[2].clicked = datetime.datetime.now()
        statistics[2].total_clicks = 1
        statistics[1].clicked = datetime.datetime.now()
        statistics[1].total_clicks = 2

        for field, expected, comment in (
                ('clicks', '2', 'Clicks'),
                ('total_clicks', 3, 'Total Clicks'),
                ('clicks_ratio', 66, 'int(100*clicks(2)/received(3))'),
                ('ctor', 100, 'int(100*clicks(2)/opened(2))'),
                ('opened_ratio', 66, 'int(opened(2)/received(3))')):
            with self.subTest(field=field):
                self.assertEqual(getattr(mass_mailing, field), expected, comment)

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
        for field, expected, comment in (
                ('bounced', '1', 'Bounced'),
                ('received', '2', 'Received'),
                ('received_ratio', 66, 'int(100*received/sent)'),
                ('bounced_ratio', 33, 'int(100*bounced/sent)')):
            with self.subTest(field=field):
                self.assertEqual(getattr(mass_mailing, field), expected, comment)

    def test_failed(self):
        """Test that failed is calculated correctly."""
        mass_mailing = create_mass_mailing(self.env)
        statistics = create_mass_mailing_statistics(self.env, mass_mailing, 3)
        statistics[2].bounced = datetime.datetime.now()
        self.assertEqual(mass_mailing.bounced, '1')

    def test_optout(self):
        """Test that optout statistics is correctly calculated."""
        mass_mailing = create_mass_mailing(self.env)
        statistics = create_mass_mailing_statistics(self.env, mass_mailing, 3)
        self.assertEqual(mass_mailing.opt_out, '1')
        self.assertEqual(mass_mailing.opt_out_ratio,
                         33,
                         'int(100*opt_out(1)/received(3))')

    def test_complicated_calculations(self):
        """Test general calculations more complicated scenarios."""
        mass_mailing = create_mass_mailing(self.env)
        statistics = create_mass_mailing_statistics(self.env, mass_mailing, 10)
        for x in range(10):
            if x >= 5:
                statistics[x].opened = False
        statistics[6].ignored = datetime.datetime.now()
        statistics[6].sent = False
        statistics[7].bounced = datetime.datetime.now()
        statistics[8].bounced = datetime.datetime.now()
        statistics[0].replied = datetime.datetime.now()
        statistics[0].clicked = datetime.datetime.now()
        statistics[0].total_clicks = 1
        statistics[1].clicked = datetime.datetime.now()
        statistics[1].total_clicks = 2
        statistics[2].clicked = datetime.datetime.now()
        statistics[2].total_clicks = 3

        for field, expected in (
                ('opened', '5'),
                ('opened_ratio', 71),  # 100*5/7 Opened/(sent - ignored - bounced)
                ('sent', '9'),
                ('ignored', 1),
                ('received', '7'),
                ('received_ratio', 77),  # 100*7/9
                ('bounced', '2'),
                ('bounced_ratio', 22),  # 100*2/9
                ('replied', 1),
                ('replied_ratio', 11),  # 100*1/9
                ('clicks', '3'),
                ('total_clicks', 6),
                ('clicks_ratio', 42),  # 100*3/7
                ('ctor', 60),  # 100*3/5
                ('opt_out', 1),
                ('opt_out_ratio', 1)):
            with self.subTest(field=field):
                self.assertEqual(getattr(mass_mailing, field), expected)
