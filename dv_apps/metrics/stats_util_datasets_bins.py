import random
import numpy as np
import pandas as pd

from django.db.models import F
from django.db import models

from dv_apps.datasets.models import DatasetVersion
from dv_apps.datafiles.models import FileMetadata


class FilesPerDatasetCounter(object):
    """Count the files in each dataset version"""

    def __init__(self):
        pass


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


    def get_latest_dataset_version_ids(self):
        """For the binning, we only want the latest dataset versions"""

        filter_params = dict()

        # -----------------------------
        # Get latest DatasetVersion ids
        # -----------------------------
        id_info_list = DatasetVersion.objects.filter(**filter_params\
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

    def get_counts(self):

        latest_dsv_ids = self.get_latest_dataset_version_ids()

        filter_params = dict(datasetversion__id__in=latest_dsv_ids)

        # Make query
        ds_version_counts = FileMetadata.objects.filter(**filter_params\
                            ).annotate(dsv_id=F('datasetversion__id'),\
                            ).values('dsv_id',\
                            ).annotate(cnt=models.Count('datafile__id')\
                            ).values('dsv_id', 'cnt'\
                            ).order_by('-cnt')

        # Convert to Dataframe
        df = pd.DataFrame(list(ds_version_counts), columns = ['dsv_id', 'cnt'])

        #print df
        #print df['cnt'].max()
        #print '-' * 10

        step_num = 10
        high_num = 200  # high_num=df['cnt'].max()+step_num

        bins = self.get_bin_list(step=step_num, low_num=0, high_num=high_num+step_num)

        # bins changing as more files added
        """bins = self.get_bin_list(step=20, low_num=0, high_num=199)
        bins += self.get_bin_list(step=100, low_num=200, high_num=999)
        bins += self.get_bin_list(step=1000, low_num=1000, high_num=df['cnt'].max()+1000)
        """

        #bins = self.get_bin_list(step=step_num, low_num=0, high_num=df['cnt'].max()+step_num)


        df['bin_label'] = pd.cut(df['cnt'], bins)

        vcounts = pd.value_counts(df['bin_label'])

        d = vcounts.to_dict()

        new_dict = {}
        for k, v in d.items():
            #if v > 0:
            sort_key = int(k[1:-1].split(',')[0])
            new_dict[sort_key] = (k, v)


        keys = new_dict.keys()
        keys.sort()
        info_list = []
        for k in keys:
            info = new_dict[k]
            #print '(%d) %s    %s' % (k, info[0], info[1])
            print '%s    %s' % (info[0], info[1])
            d = dict(sort_key=k, bin_str=info[0][1:-1], value=info[1])
            info_list.append(d)
        return info_list
