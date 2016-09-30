import pandas as pd
import json
from collections import OrderedDict

from django.db.models import F
from django.db import models

from dv_apps.datasets.models import Dataset, DatasetVersion
from dv_apps.datafiles.models import FileMetadata
from dv_apps.utils.msg_util import msgt, msg

from dv_apps.metrics.stats_util_base import StatsMakerBase
from dv_apps.metrics.stats_result import StatsResult


class StatsMakerDatasetBins(StatsMakerBase):


    def __init__(self, **kwargs):
        """Process kwargs via StatsMakerBase"""

        super(StatsMakerDatasetBins, self).__init__(**kwargs)



    def get_bin_list(self, step=10, low_num=0, high_num=100):
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


    def get_dataset_version_ids(self, **extra_filters):
        """For the binning, we only want the latest dataset versions"""

        filter_params = dict()

        # Add extra filters from kwargs, e.g. published
        #
        if extra_filters:
            for k, v in extra_filters.items():
                filter_params[k] = v

        dataset_id_filter = {}  # no filter unless published/unpublished

        if len(filter_params) > 0:
            # -----------------------------
            # Retrieve Dataset ids published/unpublished
            # -----------------------------
            dataset_ids = Dataset.objects.select_related('dvobject'\
                            ).filter(**filter_params\
                            ).values_list('dvobject__id', flat=True)

            # ok, reduce by ids...
            dataset_id_filter = dict(dataset__in=dataset_ids)


        # -----------------------------
        # Get latest DatasetVersion ids
        # -----------------------------
        id_info_list = DatasetVersion.objects.filter(**dataset_id_filter\
            ).values('id', 'dataset_id', 'versionnumber', 'minorversionnumber'\
            ).order_by('dataset_id', '-id', '-versionnumber', '-minorversionnumber')

        # -----------------------------
        # Iterate through and get the DatasetVersion id
        #        of the latest version
        # -----------------------------
        latest_dsv_ids = []
        last_dataset_id = None
        for idx, info in enumerate(id_info_list):
            if idx == 0 or info['dataset_id'] != last_dataset_id:
                latest_dsv_ids.append(info['id'])

            last_dataset_id = info['dataset_id']

        return latest_dsv_ids


    def get_file_counts_per_dataset_latest_versions_published(self):

        return self.get_file_counts_per_dataset_latest_versions(\
                    **self.get_is_published_filter_param())


    def get_file_counts_per_dataset_latest_versions_unpublished(self):

        return self.get_file_counts_per_dataset_latest_versions(\
                    **self.get_is_NOT_published_filter_param())


    def get_file_counts_per_dataset_latest_versions(self, **extra_filters):
        """
        Get binning stats for the number of files in each Dataset.
        For the counts, only use the LATEST DatasetVersion
        """

        # Get the correct DatasetVersion ids as a filter parameter
        #
        latest_dsv_ids = self.get_dataset_version_ids(**extra_filters)
        filter_params = dict(datasetversion__id__in=latest_dsv_ids)

        # Make query
        #
        ds_version_counts = FileMetadata.objects.filter(**filter_params\
                            ).annotate(dsv_id=F('datasetversion__id'),\
                            ).values('dsv_id',\
                            ).annotate(cnt=models.Count('datafile__id')\
                            ).values('dsv_id', 'cnt'\
                            ).order_by('-cnt')

        # Convert to Dataframe
        #
        df = pd.DataFrame(list(ds_version_counts), columns = ['dsv_id', 'cnt'])

        # Get the list of bins
        #
        high_num = high_num=df['cnt'].max() + self.bin_size
        bins = self.get_bin_list(step=self.bin_size, low_num=0, high_num=high_num+self.bin_size)

        # Add a new column, assigning each file count to a bin
        #
        df['bin_label'] = pd.cut(df['cnt'], bins)

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
        df_bins['bin_end'] = df_bins['bin'].apply(lambda x: int(x[1:-1].split(',')[1]))

        # Add a formatted string
        # (0, 20] -> 0 to 20
        # (20, 30] -> 20 to 30
        # etc
        df_bins['bin_str'] = df_bins['bin'].apply(lambda x: x[1:-1].replace(', ', ' to '))

        # Sort the bins
        #
        df_bins = df_bins.sort('sort_key')

        msgt(df_bins)

        # If appropriate, skip empty bins, e.g. remove 0 counts
        #
        if self.skip_empty_bins:
            df_bins = df_bins.query('count != 0')
            msg(df_bins)


        # Return as python dict
        #   # bit expensive but want orderedDict
        formatted_records_json = df_bins.to_json(orient='records')
        formatted_records = json.loads(formatted_records_json, object_pairs_hook=OrderedDict)

        data_dict = OrderedDict()
        data_dict['record_count'] = len(formatted_records)
        data_dict['records'] = formatted_records

        return StatsResult.build_success_result(data_dict)

"""
    # bins changing as more files added
    bins = self.get_bin_list(step=20, low_num=0, high_num=199)
    bins += self.get_bin_list(step=100, low_num=200, high_num=999)
    bins += self.get_bin_list(step=1000, low_num=1000, high_num=df['cnt'].max()+1000)
    #bins = self.get_bin_list(step=step_num, low_num=0, high_num=df['cnt'].max()+step_num)
"""
