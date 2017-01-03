"""
Counts of file bytes per Dataset including all published files
Answers the question: How many datasets have "x" number of bytes?

For example, if the "bin_size" is set to 1,000,000 (without commas), results will show
the number of datasets with 0bytes up to 1MB of file storage,
the number of datasets with 1MB up to 2MB of file storage, etc.
"""
import pandas as pd
import json
from collections import OrderedDict

from django.db.models import F, FloatField, Sum
from django.db import models

from dv_apps.datasets.models import Dataset, DatasetVersion
from dv_apps.datafiles.models import Datafile
from dv_apps.utils.msg_util import msgt, msg
from dv_apps.utils.byte_size import sizeof_fmt

from dv_apps.metrics.stats_util_base import StatsMakerBase
from dv_apps.metrics.stats_result import StatsResult

ONE_MILLION = 2**20 #10**6
FIFTY_MILLION = ONE_MILLION*50
ONE_HUNDRED_MILLION = ONE_MILLION*100
ONE_BILLION = ONE_MILLION**1000

class StatsMakerDatasetSizes(StatsMakerBase):
    """Answers the question: How many datasets have "x" number of bytes?
    Do we include/exclude harvested files?
    """


    def __init__(self, **kwargs):
        """Process kwargs via StatsMakerBase"""

        super(StatsMakerDatasetSizes, self).__init__(**kwargs)
        self.bin_size = FIFTY_MILLION#ONE_HUNDRED_MILLION


    def get_bin_list(self, step=FIFTY_MILLION, low_num=0, high_num=ONE_BILLION):
        assert high_num > low_num, "high_num must be greater than low_num"
        assert low_num >= 0, "low_num must be at least 0.  Cannot be negative"
        assert step > 0, "step must greater than 0"
        assert high_num > step, "step must lower than high_num"

        l = []
        next_num = low_num
        while next_num <= high_num:
            l.append(next_num)
            next_num += step
        return l


    def get_dataset_ids(self, **extra_filters):
        """For the binning, we all the files in the dataset"""

        filter_params = dict()

        # Add extra filters from kwargs, e.g. published
        #
        if extra_filters:
            for k, v in extra_filters.items():
                filter_params[k] = v

        if len(filter_params) > 0:
            # -----------------------------
            # Retrieve Dataset ids published/unpublished
            # -----------------------------
            dataset_ids = Dataset.objects.select_related('dvobject'\
                            ).filter(**filter_params\
                            ).values_list('dvobject__id', flat=True)
            return dataset_ids

        return []




    def get_dataset_size_counts_published(self):

        return self.get_dataset_size_counts(\
                    **self.get_is_published_filter_param())


    def get_dataset_size_counts_unpublished(self):

        return self.get_dataset_size_counts(\
                    **self.get_is_NOT_published_filter_param())


    def get_dataset_size_counts(self, **extra_filters):
        """
        Get binning stats for the byte size of each Dataset.
        """

        # Get the correct DatasetVersion ids as a filter parameter
        #
        dataset_ids = self.get_dataset_ids(**extra_filters)
        filter_params = dict(dvobject__id__in=dataset_ids)

        # Make query
        #
        dataset_file_sizes = Datafile.objects.annotate(ds_id=F('dvobject__owner__id'),\
                            ).values('ds_id',\
                            ).annotate(cnt=models.Count('dvobject__id')\
                                , ds_size=Sum('filesize')
                            ).values('ds_id', 'cnt', 'ds_size'\
                            ).order_by('ds_size')


        # Convert to Dataframe
        #
        df = pd.DataFrame(list(dataset_file_sizes), columns = ['dsv_id', 'cnt', 'ds_size'])

        # Get the list of bins
        #
        high_num = df['ds_size'].max() + self.bin_size_bytes

        bins = self.get_bin_list(step=self.bin_size_bytes, low_num=0, high_num=high_num+self.bin_size_bytes)

        # Add a new column, assigning each file count to a bin
        #
        df['bin_label'] = pd.cut(df['ds_size'], bins)

        # Count the occurrence of each bin
        #
        bin_count_series = pd.value_counts(df['bin_label'])

        # Make the Series into a new DataFrame
        #
        df_bins = pd.DataFrame(dict(bin=bin_count_series.index,\
                            count=bin_count_series.values))

        # Add a sort key
        # (0, 20] -> 0
        # (20, 30] -> 20
        # etc
        df_bins['sort_key'] = df_bins['bin'].apply(lambda x: int(x[1:-1].split(',')[0]))
        df_bins['bin_start_inclusive'] = df_bins['sort_key']
        df_bins['bin_start_inclusive_commas'] = df_bins['bin_start_inclusive'].apply(lambda x: "{:,}".format(x))
        df_bins['bin_start_inclusive_abbrev'] = df_bins['bin_start_inclusive'].apply(lambda x: sizeof_fmt(x))

        df_bins['bin_end'] = df_bins['bin'].apply(lambda x: int(x[1:-1].split(',')[1]))
        df_bins['bin_end_commas'] = df_bins['bin_end'].apply(lambda x: "{:,}".format(x))
        df_bins['bin_end_abbrev'] = df_bins['bin_end'].apply(lambda x: sizeof_fmt(x))


        df_bins['bin_str'] = df_bins['bin_start_inclusive_abbrev']\
                            + ' to '\
                            + df_bins['bin_end_abbrev']

        # Sort the bins
        #
        df_bins = df_bins.sort('sort_key')

        #msgt(df_bins)

        # If appropriate, skip empty bins, e.g. remove 0 counts
        #
        if self.skip_empty_bins:
            df_bins = df_bins.query('count != 0')
            #msg(df_bins)


        # Return as python dict
        #   # bit expensive but want orderedDict
        formatted_records_json = df_bins.to_json(orient='records')
        formatted_records = json.loads(formatted_records_json, object_pairs_hook=OrderedDict)

        data_dict = OrderedDict()
        data_dict['record_count'] = len(formatted_records)
        data_dict['dataset_count'] = df_bins['count'].sum()
        data_dict['records'] = formatted_records

        return StatsResult.build_success_result(data_dict)

"""
    # bins changing as more files added
    bins = self.get_bin_list(step=20, low_num=0, high_num=199)
    bins += self.get_bin_list(step=100, low_num=200, high_num=999)
    bins += self.get_bin_list(step=1000, low_num=1000, high_num=df['cnt'].max()+1000)
    #bins = self.get_bin_list(step=step_num, low_num=0, high_num=df['cnt'].max()+step_num)

python manage.py shell
from dv_apps.metrics.stats_util_dataset_size import StatsMakerDatasetSizes
s = StatsMakerDatasetSizes()
print s.get_dataset_size_counts()
"""
