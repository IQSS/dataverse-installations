"""
Note: This tabular test base is to allow use of the same data for several tests
without clearing the database.  These are read-only tests.
"""
import json
from os.path import realpath, dirname, isfile, join
import requests

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.core import management

from dv_apps.dvobjects.models import DvObject
from dv_apps.metrics.stats_util_datasets import StatsMakerDatasets
from dv_apps.metrics.stats_util_dataverses import StatsMakerDataverses
from dv_apps.metrics.stats_util_files import StatsMakerFiles


def setUpModule():
    """
    Module Set Up placeholder
    """
    pass


def tearDownModule():
    """
    Module tear down placeholder
    """
    pass


class TestMetricsBase(TestCase):
    """
    Load database once--at the beginning of subclass creation.
    All of the data is used for read-only tests so this saves considerable time.
    """
    """
    @classmethod
    def tearDownClass(cls):
        management.call_command('flush', verbosity=3, interactive=False)

    @classmethod
    def setUpClass(cls):
        management.call_command('loaddata', 'test_2016_0812.json', verbosity=3)
    """

class TestDataverseMetrics(TestMetricsBase):

    def test_01_dataverse_counts(self):
        """Test dataverse counts by month"""

        stats_result  = stats_dvs.get_dataverse_counts_by_month_published()
        print stats_result.result_data
        self.assertEqual(2510, 2510)
        """
#import ipdb; ipdb.set_trace()
if not stats_result_dv_counts.has_error():
    resp_dict['dataverse_counts_by_month'] = list(stats_result_dv_counts.result_data)
    resp_dict['dataverse_counts_by_month_sql'] = stats_result_dv_counts.sql_query

# -------------------------
# Dataverse counts by type
# -------------------------
stats_result_dv_counts_by_type =\
    stats_dvs.get_dataverse_counts_by_type_published(exclude_uncategorized=True)
if not stats_result_dv_counts_by_type.has_error():
    resp_dict['dataverse_counts_by_type'] = stats_result_dv_counts_by_type.result_data
    resp_dict['dv_counts_by_category_sql'] = stats_result_dv_counts_by_type.sql_query

        cnt = DvObject.objects.all().count()
        print 'num DvObjects', cnt
        #self.assertEqual(cnt, 21)
        self.assertEqual(cnt, 2510)
        """
