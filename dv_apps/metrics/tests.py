from django.test import TestCase
from dv_apps.metrics.stats_util_dataverses import StatsMakerDataverses

class DvObjectsTestCase(TestCase):

    #fixtures = ['test_2016_0812.json']

    def setUp(self):
        pass


    def test_01_todo(self):
        """Test to see if db created"""

        stats_maker = StatsMakerDataverses()
        stats_result = stats_maker.get_dataverse_counts_by_month()

        print 'stats_result.result_data', stats_result.result_data

        self.assertEqual(stats_result.has_error(), False)
        self.assertEqual(stats_result.result_data, [])
