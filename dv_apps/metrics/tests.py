from __future__ import print_function

from dv_apps.metrics.metrics_test_base import MetricsTestBase

from dv_apps.metrics.stats_util_dataverses import StatsMakerDataverses
from dv_apps.metrics.stats_util_datasets import StatsMakerDatasets
from dv_apps.metrics.stats_util_files import StatsMakerFiles


class MetricsCountTests(MetricsTestBase):
    """
    Test metrics from StatsMakerDataverses
    Note: MetricsTestBase loads 10k+ objects from fixtures
    """

    def test_data_params(self):
        """Test date params"""
        pass

    def test_01_dataverse_total_counts(self):
        """Count total dataverses: published, unpublished, all"""
        print ('Count total dataverses: published, unpublished, all')

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
        """Test published dataverse counts by month"""
        print ('Test published dataverse counts by month')

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
        """Test unpublished dataverse counts by month"""
        print ('Test unpublished dataverse counts by month')

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
        """Test all dataverse counts by month"""
        print ('Test all dataverse counts by month')

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
        """Count total datasets: published, unpublished, all"""
        print ('Count total datasets: published, unpublished, all')

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
        """Test published dataset counts by month"""
        print ('Test published dataset counts by month')

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
        """Test unpublished dataset counts by month"""
        print ('Test unpublished dataset counts by month')

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
        """Test all dataset counts by month"""
        print ('Test all dataset counts by month')

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
        """Count total files: published, unpublished, all"""
        print ('Count total files: published, unpublished, all')

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
        """File downloads by month: published,"""
        print ('File downloads by month: published')

        kwargs = dict(start_date='2015-05-30',\
                    end_date='2015-10-01')
        stats_maker = StatsMakerFiles(**kwargs)

        r = stats_maker.get_file_downloads_by_month_published()

        # check number of months
        self.assertEqual(len(r.result_data), 4)

        # check last month
        last_month = {'cnt': 6,
             'month_name': 'Sep',
             'month_num': 9,
             'running_total': 125,
             'year_num': 2015,
             'yyyy_mm': '2015-09'}
        self.assertEqual(r.result_data[-1], last_month)


    def test_10_file_downloads_by_month_unpublished(self):
        """File downloads by month: unpublished,"""
        print ('File downloads by month: unpublished')

        kwargs = dict(start_date='2015-02-01',\
                    end_date='2015-11-01')

        stats_maker = StatsMakerFiles(**kwargs)
        r = stats_maker.get_file_downloads_by_month_unpublished()

        # check number of months
        self.assertEqual(len(r.result_data), 0)

        # check data -- very rare to have downloaded "unpublished" files
        self.assertEqual(r.result_data, [])

    def test_12_file_downloads_by_month_all(self):
        """File downloads by month: all"""
        print ('File downloads by month: all')

        kwargs = dict(selected_year=2015)
        stats_maker = StatsMakerFiles(**kwargs)
        r = stats_maker.get_file_downloads_by_month()

        # check number of months
        self.assertEqual(len(r.result_data), 9)

        # check last month
        last_month = {'cnt': 22,
             'month_name': 'Dec',
             'month_num': 12,
             'running_total': 237,
             'year_num': 2015,
             'yyyy_mm': '2015-12'}
        self.assertEqual(r.result_data[-1], last_month)
