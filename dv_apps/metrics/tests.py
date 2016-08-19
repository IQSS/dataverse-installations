from django.test import TestCase
from django.core import management

from dv_apps.metrics.stats_util_dataverses import StatsMakerDataverses
from dv_apps.dataverses.models import Dataverse

class MetricsTestBase(TestCase):
    """
    Load database once--at the beginning of subclass creation.
    All of the data is used for read-only tests so this saves considerable time.
    """

    @classmethod
    def setUpClass(cls):
        print 'load db'
        management.call_command('loaddata', 'test_2016_0819.json', verbosity=3)

    @classmethod
    def tearDownClass(cls):
        print 'flush db'
        management.call_command('flush', verbosity=3, interactive=False)


class MetricsCase(MetricsTestBase):

    fixtures = ['test_2016_0812.json']

    def setUp(self):
        pass


    def test_01_todo(self):
        """Test to see if db created"""
        print '--- TEST 1 ---'

        stats_maker = StatsMakerDataverses()
        stats_result = stats_maker.get_dataverse_counts_by_month()

        #print 'stats_result.result_data', stats_result.result_data
        print 'stats_result.result_data', len(stats_result.result_data)

        num_dvs = Dataverse.objects.all().count()
        self.assertEqual(num_dvs, 356)


        self.assertEqual(stats_result.has_error(), False)
        # 16 stats info objects
        self.assertEqual(len(stats_result.result_data), 16)

        # 1st object
        first_object = stats_result.result_data[0]
        self.assertEqual(first_object['cnt'], 39)
        self.assertEqual(first_object['running_total'], 39)
        self.assertEqual(first_object['yyyy_mm'], '2015-04')

        # 2nd object
        first_object = stats_result.result_data[1]
        self.assertEqual(first_object['cnt'], 29)
        self.assertEqual(first_object['running_total'], 68)
        self.assertEqual(first_object['yyyy_mm'], '2015-05')


    def test_02_todo(self):
        """Test to see if db created"""
        print '--- TEST 2 ---'
        num_dvs = Dataverse.objects.all().count()
        self.assertEqual(num_dvs, 356)
