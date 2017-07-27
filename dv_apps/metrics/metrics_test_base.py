from __future__ import print_function
from django.test import TestCase
from django.core import management


class MetricsTestBase(TestCase):
    """
    Load database once--at the beginning of subclass creation.
    All of the data is used for read-only tests so this saves considerable time.
    """

    @classmethod
    def setUpClass(cls):
        print ('load fixtures')
        management.call_command('loaddata', 'test_2017_0727.json', verbosity=3)

    @classmethod
    def tearDownClass(cls):
        print ('flush fixtures')
        management.call_command('flush', verbosity=3, interactive=False)
