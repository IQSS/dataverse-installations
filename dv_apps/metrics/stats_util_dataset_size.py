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

from dv_apps.metrics.stats_util_base import StatsMakerBase,\
        BYTES_ONE_MILLION,\
        BYTES_FIFTY_MILLION,\
        BYTES_ONE_HUNDRED_MILLION,\
        BYTES_ONE_BILLION

from dv_apps.metrics.stats_result import StatsResult


class StatsMakerDatasetSizes(StatsMakerBase):
    """Answers the question: How many datasets have "x" number of bytes?
    Do we include/exclude harvested files?
    """


    def __init__(self, **kwargs):
        """Process kwargs via StatsMakerBase"""
        super(StatsMakerDatasetSizes, self).__init__(**kwargs)


    def get_bin_list(self, step=BYTES_FIFTY_MILLION, low_num=0, high_num=BYTES_ONE_BILLION):
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
        filter_params = {}
        if extra_filters:
            filter_params.update(extra_filters)
        # Make query
        #
        dataset_file_sizes = Datafile.objects.filter(**filter_params\
                            ).annotate(ds_id=F('dvobject__owner__id'),\
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


        total_dataset_count = df_bins['count'].sum()


        # Add a sort key
        # (0, 20] -> 0
        # (20, 30] -> 20
        # etc
        df_bins['sort_key'] = df_bins['bin'].apply(lambda x: int(x[1:-1].split(',')[0]))

        if total_dataset_count > 0:
            df_bins['percentage_of_datasets'] = df_bins['count'].apply(lambda x: "{0:.4f}%".format(100 * x/float(total_dataset_count)))
        #100*x/float(x.sum())

        df_bins['bin_start_inclusive'] = df_bins['sort_key']
        df_bins['bin_start_inclusive_commas'] = df_bins['bin_start_inclusive'].apply(lambda x: "{:,}".format(x))
        df_bins['bin_start_inclusive_abbrev'] = df_bins['bin_start_inclusive'].apply(lambda x: sizeof_fmt(x))

        df_bins['bin_end'] = df_bins['bin'].apply(lambda x: int(x[1:-1].split(',')[1]))
        df_bins['bin_end_commas'] = df_bins['bin_end'].apply(lambda x: "{:,}".format(x))
        df_bins['bin_end_abbrev'] = df_bins['bin_end'].apply(lambda x: sizeof_fmt(x))

        df_bins['bin_str'] = df_bins['bin_start_inclusive_abbrev'].str.cat(df_bins['bin_end_abbrev'].values.astype(str), sep=' to ')

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
        data_dict['dataset_count'] = total_dataset_count
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
