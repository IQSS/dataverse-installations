"""
Tests for the metrics functions.
Note: This loads 10,000+ objects and uses them for all of the tests

Example of calling a single test:
python manage.py test dv_apps.metrics.tests.MetricsCountTests.test_date_params

"""
from __future__ import print_function

from collections import OrderedDict

from dv_apps.metrics.metrics_test_base import MetricsTestBase
from dv_apps.metrics.stats_util_dataverses import StatsMakerDataverses
from dv_apps.metrics.stats_util_datasets import StatsMakerDatasets
from dv_apps.metrics.stats_util_files import StatsMakerFiles,\
    FILE_TYPE_OCTET_STREAM



class MetricsCountTests(MetricsTestBase):
    """
    Test metrics from StatsMakerDataverses
    Note: MetricsTestBase loads 10k+ objects from fixtures
    """

    def try_data_params(self, **params):
        """Used for checking date param logic"""

        stats_maker = StatsMakerDataverses(**params)
        r = stats_maker.get_dataverse_count_published()
        return r


    def test_00_date_params(self):
        """Test date params"""
        print (self.test_00_date_params.__doc__)

        # Note: All date param checking is in parent class StatsMakerBase
        #   e.g. it's the same in:
        #     StatsMakerDataverses, StatsMakerDatasets, and StatsMakerFiles
        #

        # Year cannot be zero
        kwargs = dict(selected_year=0)
        r = self.try_data_params(**kwargs)
        self.assertEqual(r.has_error(), True)
        self.assertEqual(r.error_message, 'The year cannot be zero.')

        # Year cannot be negative
        kwargs = dict(selected_year=-1)
        r = self.try_data_params(**kwargs)
        self.assertEqual(r.has_error(), True)
        self.assertEqual(r.error_message, 'The year must be digits.')

        kwargs = dict(selected_year='-1')
        r = self.try_data_params(**kwargs)
        self.assertEqual(r.has_error(), True)
        self.assertEqual(r.error_message, 'The year must be digits.')

        # Year cannot be a 'dog'
        kwargs = dict(selected_year='dog')
        r = self.try_data_params(**kwargs)
        self.assertEqual(r.has_error(), True)
        self.assertEqual(r.error_message, 'The year must be digits.')

        # Year CAN be 9999
        kwargs = dict(selected_year=9999)
        r = self.try_data_params(**kwargs)
        self.assertEqual(r.has_error(), False)

        # Not more than 4-digit year
        kwargs = dict(selected_year=10000)
        r = self.try_data_params(**kwargs)
        self.assertEqual(r.has_error(), True)
        self.assertEqual(r.error_message, 'The year cannot be more than 4-digits (YYYY)')

        # Not more than 4-digit year (as a string)
        kwargs = dict(selected_year='10000')
        r = self.try_data_params(**kwargs)
        self.assertEqual(r.has_error(), True)
        self.assertEqual(r.error_message, 'The year cannot be more than 4-digits (YYYY)')

        # Bad year - '123'
        kwargs = dict(start_date='123-02-01')
        r = self.try_data_params(**kwargs)
        self.assertEqual(r.has_error(), True)
        self.assertEqual(r.error_message, 'Start date is invalid.  Use YYYY-MM-DD format.')

        # Bad year - '0000'
        kwargs = dict(start_date='0000-02-1')
        r = self.try_data_params(**kwargs)
        self.assertEqual(r.has_error(), True)
        self.assertEqual(r.error_message, 'Start date is invalid.  Use YYYY-MM-DD format.')

        # OK year - '0001', with day '1'
        kwargs = dict(start_date='0001-02-1')
        r = self.try_data_params(**kwargs)
        self.assertEqual(r.has_error(), False)

        # Bad day.  31st day of Feb
        kwargs = dict(start_date='1968-02-31')
        r = self.try_data_params(**kwargs)
        self.assertEqual(r.has_error(), True)
        self.assertEqual(r.error_message, 'Start date is invalid.  Use YYYY-MM-DD format.')

        # End date (uses same function as start date check)
        # Bad day. 14th month
        kwargs = dict(end_date='1968-14-01')
        r = self.try_data_params(**kwargs)
        self.assertEqual(r.has_error(), True)
        self.assertEqual(r.error_message, 'End date is invalid.  Use YYYY-MM-DD format.')

        # OK - start day / end day
        kwargs = dict(start_date='2000-01-01',\
                    end_date='2000-01-02')
        r = self.try_data_params(**kwargs)
        self.assertEqual(r.has_error(), False)

        # OK - start day / end day - same day
        kwargs = dict(start_date='2000-01-01',\
                    end_date='2000-01-01')
        r = self.try_data_params(**kwargs)
        self.assertEqual(r.has_error(), False)

        # Bad - start day / end day
        kwargs = dict(start_date='2010-01-01',\
                    end_date='1968-12-01')
        r = self.try_data_params(**kwargs)
        self.assertEqual(r.has_error(), True)
        self.assertEqual(r.error_message, 'The start date cannot be after the end date.')

        # Bad - start day / end day
        kwargs = dict(start_date='2010-01-02',\
                    end_date='2010-01-01')
        r = self.try_data_params(**kwargs)
        self.assertEqual(r.has_error(), True)
        self.assertEqual(r.error_message, 'The start date cannot be after the end date.')

        # Bad selected_year, start_date combo
        kwargs = dict(start_date='2015-01-02',\
                    selected_year=2014)
        r = self.try_data_params(**kwargs)
        self.assertEqual(r.has_error(), True)
        self.assertEqual(r.error_message, "The 'selected_year' (2014)' cannot be before the 'start_date' year (2015-01-02)")

        # OK selected_year, start_date combo. selected_year not needed, but ok
        kwargs = dict(start_date='2015-03-02',\
                    selected_year=2015)
        r = self.try_data_params(**kwargs)
        self.assertEqual(r.has_error(), False)

        # Bad selected_year, end_date combo
        kwargs = dict(end_date='2012-01-02',\
                    selected_year=2014)
        r = self.try_data_params(**kwargs)
        self.assertEqual(r.has_error(), True)
        self.assertEqual(r.error_message, "The 'selected_year' (2014)' cannot be after the 'end_date' year (2012-01-02)")


    def test_01_dataverse_total_counts(self):
        """01 - Count total dataverses: published, unpublished, all"""
        print (self.test_01_dataverse_total_counts.__doc__)

        stats_maker = StatsMakerDataverses()

        # Count published dataverse
        r = stats_maker.get_dataverse_count_published()
        self.assertEqual(r.result_data, 187)

        # Count unpublished dataverse
        r = stats_maker.get_dataverse_count_unpublished()
        self.assertEqual(r.result_data, 169)

        # Count all dataverses
        r = stats_maker.get_dataverse_count()
        self.assertEqual(r.result_data, 356)



    def test_02_dataverse_counts_by_month_published(self):
        """02 - Test published dataverse counts by month"""
        print (self.test_02_dataverse_counts_by_month_published.__doc__)

        kwargs=dict(selected_year=2016)
        stats_maker = StatsMakerDataverses(**kwargs)

        r = stats_maker.get_dataverse_counts_by_month_published()

        # check number of months
        self.assertEqual(len(r.result_data), 7)

        # check 1st month
        first_month = {'cnt': 5,
         'month_name': 'Jan',
         'month_num': 1,
         'running_total': 131,
         'year_num': 2016,
         'yyyy_mm': '2016-01'}
        self.assertEqual(r.result_data[0], first_month)

        # check last month
        last_month = {'cnt': 4,
             'month_name': 'Jul',
             'month_num': 7,
             'running_total': 187,
             'year_num': 2016,
             'yyyy_mm': '2016-07'}
        self.assertEqual(r.result_data[-1], last_month)



    def test_03_dataverse_counts_by_month_unpublished(self):
        """03 - Test unpublished dataverse counts by month"""
        print (self.test_03_dataverse_counts_by_month_unpublished.__doc__)

        stats_maker = StatsMakerDataverses()

        r = stats_maker.get_dataverse_counts_by_month_unpublished()

        # check number of months
        self.assertEqual(len(r.result_data), 16)

        # check 1st month
        first_month = {'cnt': 13,
             'month_name': 'Apr',
             'month_num': 4,
             'running_total': 13,
             'year_num': 2015,
             'yyyy_mm': '2015-04'}
        self.assertEqual(r.result_data[0], first_month)

        # check last month
        last_month = {'cnt': 6,
             'month_name': 'Jul',
             'month_num': 7,
             'running_total': 169,
             'year_num': 2016,
             'yyyy_mm': '2016-07'}
        self.assertEqual(r.result_data[-1], last_month)


    def test_04_dataverse_counts_by_month_all(self):
        """04 - Test all dataverse counts by month"""
        print (self.test_04_dataverse_counts_by_month_all.__doc__)

        stats_maker = StatsMakerDataverses()

        r = stats_maker.get_dataverse_counts_by_month()

        # check number of months
        self.assertEqual(len(r.result_data), 16)

        # check 1st month
        first_month = {'cnt': 39,
             'month_name': 'Apr',
             'month_num': 4,
             'running_total': 39,
             'year_num': 2015,
             'yyyy_mm': '2015-04'}
        self.assertEqual(r.result_data[0], first_month)

        # check last month
        last_month = {'cnt': 10,
             'month_name': 'Jul',
             'month_num': 7,
             'running_total': 356,
             'year_num': 2016,
             'yyyy_mm': '2016-07'}
        self.assertEqual(r.result_data[-1], last_month)

    def test_05_dataset_total_counts(self):
        """05 - Count total datasets: published, unpublished, all"""
        print (self.test_05_dataset_total_counts.__doc__)

        kwargs=dict(start_date='2016-01-01')
        stats_maker = StatsMakerDatasets(**kwargs)

        # Count published dataset
        r = stats_maker.get_dataset_count_published()
        self.assertEqual(r.result_data, 85)

        # Count unpublished dataset
        r = stats_maker.get_dataset_count_unpublished()
        self.assertEqual(r.result_data, 198)

        # Count all datasets
        r = stats_maker.get_dataset_count()
        self.assertEqual(r.result_data, 283)


    def test_06_dataset_counts_published(self):
        """06 - Test published dataset counts by month"""
        print (self.test_06_dataset_counts_published.__doc__)

        stats_maker = StatsMakerDatasets()

        r = stats_maker.get_dataset_counts_by_create_date_published()

        # check number of months
        self.assertEqual(len(r.result_data), 16)

        # check 1st month
        first_month = {'cnt': 21,
         'month_name': 'Apr',
         'month_num': 4,
         'running_total': 21,
         'year_num': 2015,
         'yyyy_mm': '2015-04'}
        self.assertEqual(r.result_data[0], first_month)

        # check last month
        last_month = {'cnt': 4,
         'month_name': 'Jul',
         'month_num': 7,
         'running_total': 227,
         'year_num': 2016,
         'yyyy_mm': '2016-07'}
        self.assertEqual(r.result_data[-1], last_month)

    def test_07_dataset_counts_unpublished(self):
        """07 - Test unpublished dataset counts by month"""
        print (self.test_07_dataset_counts_unpublished.__doc__)

        stats_maker = StatsMakerDatasets()

        r = stats_maker.get_dataset_counts_by_create_date_unpublished()

        # check number of months
        self.assertEqual(len(r.result_data), 16)

        # check 1st month
        first_month = {'cnt': 15,
         'month_name': 'Apr',
         'month_num': 4,
         'running_total': 15,
         'year_num': 2015,
         'yyyy_mm': '2015-04'}
        self.assertEqual(r.result_data[0], first_month)

        # check last month
        last_month = {'cnt': 94,
             'month_name': 'Jul',
             'month_num': 7,
             'running_total': 343,
             'year_num': 2016,
             'yyyy_mm': '2016-07'}
        self.assertEqual(r.result_data[-1], last_month)

    def test_08_dataset_counts_all(self):
        """08 - Test all dataset counts by month"""
        print (self.test_08_dataset_counts_all.__doc__)

        stats_maker = StatsMakerDatasets()

        r = stats_maker.get_dataset_counts_by_create_date()

        # check number of months
        self.assertEqual(len(r.result_data), 16)

        # check 1st month
        first_month = {'cnt': 36,
             'month_name': 'Apr',
             'month_num': 4,
             'running_total': 36,
             'year_num': 2015,
             'yyyy_mm': '2015-04'}
        self.assertEqual(r.result_data[0], first_month)

        # check last month
        last_month = {'cnt': 98,
             'month_name': 'Jul',
             'month_num': 7,
             'running_total': 570,
             'year_num': 2016,
             'yyyy_mm': '2016-07'}
        self.assertEqual(r.result_data[-1], last_month)


    def test_09_file_total_counts(self):
        """09 - Count total files: published, unpublished, all"""
        print (self.test_09_file_total_counts.__doc__)

        stats_maker = StatsMakerFiles()

        # Count published file
        r = stats_maker.get_datafile_count_published()
        self.assertEqual(r.result_data, 1014)

        # Count unpublished file
        r = stats_maker.get_datafile_count_unpublished()
        self.assertEqual(r.result_data, 570)

        # Count all files
        r = stats_maker.get_datafile_count()
        self.assertEqual(r.result_data, 1584)

    def test_10_file_downloads_by_month_published(self):
        """10 - File downloads by month: published,"""
        print (self.test_10_file_downloads_by_month_published.__doc__)

        kwargs = dict(start_date='2015-05-30',\
                    end_date='2015-10-01')
        stats_maker = StatsMakerFiles(**kwargs)

        r = stats_maker.get_file_downloads_by_month_published()

        # check number of months
        self.assertEqual(len(r.result_data), 5)

        # check last month
        last_month = {'cnt': 7,
             'month_name': 'Sep',
             'month_num': 9,
             'running_total': 309,
             'year_num': 2015,
             'yyyy_mm': '2015-09'}
        self.assertEqual(r.result_data[-1], last_month)


    def test_11_file_downloads_by_month_unpublished(self):
        """11 - File downloads by month: unpublished,"""
        print (self.test_11_file_downloads_by_month_unpublished.__doc__)

        kwargs = dict(start_date='2015-02-01',\
                    end_date='2015-11-01')

        stats_maker = StatsMakerFiles(**kwargs)
        r = stats_maker.get_file_downloads_by_month_unpublished()

        # check number of months
        self.assertEqual(len(r.result_data), 0)

        # check data -- very rare to have downloaded "unpublished" files
        self.assertEqual(r.result_data, [])

    def test_12_file_downloads_by_month_all(self):
        """12 - File downloads by month: all"""
        print (self.test_12_file_downloads_by_month_all.__doc__)

        kwargs = dict(selected_year=2015)
        stats_maker = StatsMakerFiles(**kwargs)
        r = stats_maker.get_file_downloads_by_month()

        # check number of months
        self.assertEqual(len(r.result_data), 9)

        # check last month
        last_month = {'cnt': 31,
             'month_name': 'Dec',
             'month_num': 12,
             'running_total': 465,
             'year_num': 2015,
             'yyyy_mm': '2015-12'}
        self.assertEqual(r.result_data[-1], last_month)

    def test_13_file_content_types_published(self):
        """13 - Content types of published files"""
        print (self.test_13_file_content_types_published.__doc__)

        kwargs = dict(start_date='2015-11-01',
                    end_date='2016-03-01')
        stats_maker = StatsMakerFiles(**kwargs)
        r = stats_maker.get_datafile_content_type_counts_published()

        # check number of entries
        self.assertEqual(len(r.result_data), 18)

        # check first listing
        first_listing = {'contenttype': u'application/octet-stream',
             'percent_string': '65.1%',
             'short_content_type': u'octet-stream',
             'total_count': 255,
             'type_count': 166}
        self.assertEqual(r.result_data[0], first_listing)

        # check 3rd listing
        third_listing = {'contenttype': u'text/tab-separated-values',
         'percent_string': '9.0%',
         'short_content_type': u'tab-separated-values',
         'total_count': 255,
         'type_count': 23}
        self.assertEqual(r.result_data[2], third_listing)


    def test_14_file_content_types_unpublished(self):
        """14 - Content types of published files"""
        print (self.test_14_file_content_types_unpublished.__doc__)

        kwargs = dict(start_date='2015-11-01',
                    end_date='2016-03-01')
        stats_maker = StatsMakerFiles(**kwargs)
        r = stats_maker.get_datafile_content_type_counts_unpublished()

        # check number of entries
        self.assertEqual(len(r.result_data), 19)

        # check first listing
        first_listing = {'contenttype': u'image/jpeg',
             'percent_string': '45.2%',
             'short_content_type': u'jpeg',
             'total_count': 126,
             'type_count': 57}
        self.assertEqual(r.result_data[0], first_listing)

        # check 3rd listing
        third_listing = {'contenttype': u'text/plain',
             'percent_string': '10.3%',
             'short_content_type': u'plain',
             'total_count': 126,
             'type_count': 13}
        self.assertEqual(r.result_data[2], third_listing)

    def test_15_file_content_types_all(self):
        """15 - Content types of all files"""
        print (self.test_15_file_content_types_all.__doc__)

        kwargs = dict(start_date='2015-11-01',
                    end_date='2016-03-01')
        stats_maker = StatsMakerFiles(**kwargs)
        r = stats_maker.get_datafile_content_type_counts()

        # check number of entries
        self.assertEqual(len(r.result_data), 25)

        # check first listing
        first_listing = {'contenttype': u'application/octet-stream',
             'percent_string': '43.6%',
             'short_content_type': u'octet-stream',
             'total_count': 381,
             'type_count': 166}
        self.assertEqual(r.result_data[0], first_listing)

        # check 3rd listing
        third_listing = {'contenttype': u'text/tab-separated-values',
             'percent_string': '12.9%',
             'short_content_type': u'tab-separated-values',
             'total_count': 381,
             'type_count': 49}
        self.assertEqual(r.result_data[2], third_listing)



    def test_16_dataverse_types_published(self):
        """16 - Affiliations of published dataverses types"""
        print (self.test_16_dataverse_types_published.__doc__)

        kwargs = dict(select_year=2016)
        stats_maker = StatsMakerDataverses(**kwargs)
        r = stats_maker.get_dataverse_counts_by_type_published()

        # check number of entries
        self.assertEqual(len(r.result_data), 6)

        # check first listing
        first_listing = {'dataversetype': u'RESEARCHERS',
              'dataversetype_label': u'RESEARCHERS',
              'percent_string': '34.0%',
              'total_count': 153,
              'type_count': 52}
        self.assertEqual(r.result_data[0], first_listing)

        # check last listing
        last_listing = {'dataversetype': u'RESEARCH_GROUP',
             'dataversetype_label': u'RESEARCH GROUP',
             'percent_string': '1.3%',
             'total_count': 153,
             'type_count': 2}
        self.assertEqual(r.result_data[-1], last_listing)

        # -------------------------
        # Include UNCATEGORIZED Dataverses
        # -------------------------
        kwargs = dict(select_year=2016)
        stats_maker = StatsMakerDataverses(**kwargs)
        r = stats_maker.get_dataverse_counts_by_type_published(exclude_uncategorized=False)

        # check number of entries
        self.assertEqual(len(r.result_data), 7)

        # check UNCATEGORIZED listing
        uncat_listing = {'dataversetype': u'UNCATEGORIZED',
             'dataversetype_label': u'UNCATEGORIZED',
             'percent_string': '18.2%',
             'total_count': 187,
             'type_count': 34}
        self.assertEqual(r.result_data[3], uncat_listing)



    def test_17_dataverse_types_unpublished(self):
        """17 - Affiliations of unpublished dataverses types"""
        print (self.test_17_dataverse_types_unpublished.__doc__)

        kwargs = dict(select_year=2016)
        stats_maker = StatsMakerDataverses(**kwargs)
        r = stats_maker.get_dataverse_counts_by_type_unpublished()

        # check number of entries
        self.assertEqual(len(r.result_data), 6)

        # check first listing
        first_listing = {'dataversetype': u'RESEARCHERS',
             'dataversetype_label': u'RESEARCHERS',
             'percent_string': '44.2%',
             'total_count': 138,
             'type_count': 61}
        self.assertEqual(r.result_data[0], first_listing)

        # check last listing
        last_listing = {'dataversetype': u'LABORATORY',
             'dataversetype_label': u'LABORATORY',
             'percent_string': '0.7%',
             'total_count': 138,
             'type_count': 1}

        self.assertEqual(r.result_data[-1], last_listing)

        # -------------------------
        # Include UNCATEGORIZED Dataverses
        # -------------------------
        kwargs = dict(select_year=2016)
        stats_maker = StatsMakerDataverses(**kwargs)
        r = stats_maker.get_dataverse_counts_by_type_unpublished(exclude_uncategorized=False)

        # check number of entries
        self.assertEqual(len(r.result_data), 7)

        # check UNCATEGORIZED listing
        uncat_listing =  {'dataversetype': u'UNCATEGORIZED',
              'dataversetype_label': u'UNCATEGORIZED',
              'percent_string': '18.3%',
              'total_count': 169,
              'type_count': 31}
        self.assertEqual(r.result_data[2], uncat_listing)

    def test_18_dataverse_types_all(self):
        """18 - Affiliations of all dataverses types"""
        print (self.test_18_dataverse_types_all.__doc__)

        kwargs = dict(select_year=2016)
        stats_maker = StatsMakerDataverses(**kwargs)
        r = stats_maker.get_dataverse_counts_by_type()

        # check number of entries
        self.assertEqual(len(r.result_data), 7)

        # check first listing
        first_listing = {'dataversetype': u'RESEARCHERS',
              'dataversetype_label': u'RESEARCHERS',
              'percent_string': '38.8%',
              'total_count': 291,
              'type_count': 113}
        self.assertEqual(r.result_data[0], first_listing)

        # check last listing
        last_listing =  {'dataversetype': u'LABORATORY',
              'dataversetype_label': u'LABORATORY',
              'percent_string': '0.3%',
              'total_count': 291,
              'type_count': 1}

        self.assertEqual(r.result_data[-1], last_listing)

        # -------------------------
        # Include UNCATEGORIZED Dataverses
        # -------------------------
        kwargs = dict(select_year=2016)
        stats_maker = StatsMakerDataverses(**kwargs)
        r = stats_maker.get_dataverse_counts_by_type(exclude_uncategorized=False)

        # check number of entries
        self.assertEqual(len(r.result_data), 8)

        # check UNCATEGORIZED listing
        uncat_listing =   {'dataversetype': u'UNCATEGORIZED',
          'dataversetype_label': u'UNCATEGORIZED',
          'percent_string': '18.3%',
          'total_count': 356,
          'type_count': 65}
        self.assertEqual(r.result_data[2], uncat_listing)


    def test_19_file_extensions_within_type(self):
        """19 - File extensions within type"""
        print (self.test_19_file_extensions_within_type.__doc__)

        stats_maker = StatsMakerFiles()
        r = stats_maker.view_file_extensions_within_type(file_type=FILE_TYPE_OCTET_STREAM)

        num_unique_extensions = r.result_data.get('number_unique_extensions')

        # check number of extensions
        #
        self.assertEqual(num_unique_extensions, 67)

        # check that list length matches number of extensions
        #
        ext_counts = r.result_data.get('file_extension_counts', [])
        self.assertEqual(len(ext_counts), 67)

        # check 5th listing in extension count list
        #
        listing_5 = OrderedDict([('extension', u'.xlsx'),
                    ('count', 24),
                    ('total_count', 667),
                    ('percent_string', '3.598%')])

        self.assertEqual(listing_5, ext_counts[4])
