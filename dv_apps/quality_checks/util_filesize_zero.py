"""
Checks for filesizes with zero or null

Expected:
    Local files:with size zero
      - No local files with size null
      -
           No harvested files size zero


"""
from collections import OrderedDict

from dv_apps.datasets.models import Dataset, DatasetVersion
from dv_apps.datafiles.models import Datafile, FileMetadata
from django.db.models import Q

class NamedStat(object):

    def __init__(self, name, stat, desc=None):
        self.name = name
        self.stat = stat
        self.desc = desc

class ZeroFilesizeStats(object):

    def __init__(self):
        pass


    @staticmethod
    def get_local_files_no_size():

        # Dataset ids - non-Harvested
        ds_ids_local = Dataset.objects.filter(harvestingclient__isnull=True\
                                        ).values_list('dvobject__id', flat=True)

        Datafile.objects.select_related('dvobject'\
                ).filter(Q(filesize=0) | Q(filesize__isnull=True),
                ).filter(dvobject__owner_id__in=ds_ids_local)



    @staticmethod
    def get_basic_stats():

        # Dataset ids - Harvested
        ds_ids_harvested = Dataset.objects.filter(harvestingclient__isnull=False\
                                        ).values_list('dvobject__id', flat=True)

        # Dataset ids - local
        ds_ids_local = Dataset.objects.filter(harvestingclient__isnull=True\
                                        ).values_list('dvobject__id', flat=True)

        # ---------------------
        # Harvested file counts
        # ---------------------

        #cnt_harvested_null = Datafile.objects.filter(\
        #                    filesize__isnull=True,
        #                    dvobject__owner_id__in=ds_ids_harvested).count()

        cnt_harvested_zero = Datafile.objects.filter(\
                            filesize=0,
                            dvobject__owner_id__in=ds_ids_harvested).count()

        #cnt_harvested_zero_null = cnt_harvested_null + cnt_harvested_zero

        # ---------------------
        # Local file counts
        # ---------------------

        """
        cnt_local_null = Datafile.objects.filter(\
                            filesize__isnull=True,
                            dvobject__owner_id__in=ds_ids_local).count()

        cnt_local_zero = Datafile.objects.filter(\
                            filesize=0,
                            dvobject__owner_id__in=ds_ids_local).count()
        """
        cnt_local_zero_null = Datafile.objects.filter(\
                            Q(filesize=0) | Q(filesize__isnull=True),
                            dvobject__owner_id__in=ds_ids_local).count()

        file_stats = dict(\
            cnt_local_zero_null=NamedStat(\
                                'Filesize 0 or null (Local)',
                                cnt_local_zero_null,
                                ('Count of local Datafiles with a'
                                 ' recorded size of 0 bytes or null')),

            cnt_harvested_zero=NamedStat(\
                                'Filesize 0 or null (Harvested)',
                                cnt_harvested_zero,
                                ('Count of harvested Datafiles with a'
                                 ' recorded size of 0 bytes or null')),
            #cnt_local_null=NamedStat('Local file size is null', cnt_local_null),
            #cnt_local_zero=NamedStat('Local file size is zero', cnt_harvested_zero),
            #cnt_harvested_zero_null=NamedStat('Harvested file size is zero or null',
            #                                  cnt_harvested_zero_null),
            #cnt_harvested_null=NamedStat('Harvested file size is null', cnt_harvested_null),
            )

        return file_stats



"""Fizesize is null

All: 31,177 (1c)
Local: 125  (1b)
Harvested: 31,052 (1c)

---

Fizesize is 0

All: 108,156 (2a)
Local: 493 (2b)
Harvested: 107,663 (2c)

---

(1a) ```Select count(*) from datafile where filesize is null;```

(1b) ```select count(df.id) from datafile df, dvobject dv
where df.filesize is null
and df.id = dv.id
and dv.owner_id in (select id from dataset where harvestingclient_id is not null);```

(1c) ```select count(df.id) from datafile df, dvobject dv
where df.filesize is null
and df.id = dv.id
and dv.owner_id in (select id from dataset where harvestingclient_id is null);```

---

(2a) ```Select count(*) from datafile where filesize = 0;```

(2b) ```select count(df.id) from datafile df, dvobject dv
where df.filesize = 0
and df.id = dv.id
and dv.owner_id in (select id from dataset where harvestingclient_id is null);```

(2c) ```select count(df.id) from datafile df, dvobject dv
where df.filesize = 0
and df.id = dv.id
and dv.owner_id in (select id from dataset where harvestingclient_id is not null);```
"""
