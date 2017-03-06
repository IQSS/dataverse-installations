"""
Checks for files missing a checksum
"""
from dv_apps.datasets.models import Dataset#, DatasetVersion
from dv_apps.datafiles.models import Datafile#, FileMetadata
from django.db.models import Q
from dv_apps.quality_checks.named_stat import NamedStat

class NoChecksumStats(object):
    """Checks for files with no checksum"""

    def __init__(self):
        pass


    @staticmethod
    def get_files_no_checksum(harvested_only=False):
        """Return a list of Datafile objects missing the checksum"""

        dataset_ids = Dataset.objects.filter(\
                        harvestingclient__isnull=not harvested_only\
                        ).values_list('dvobject__id', flat=True)

        total_cnt = Datafile.objects.select_related('dvobject'\
                ).filter(Q(checksumvalue='') | Q(checksumvalue__isnull=True),
                ).filter(dvobject__owner_id__in=dataset_ids\
                ).count()

        view_limit = 4

        dfiles = Datafile.objects.select_related('dvobject'\
                ).filter(Q(checksumvalue='') | Q(checksumvalue__isnull=True),
                ).filter(dvobject__owner_id__in=dataset_ids\
                ).order_by('dvobject__owner_id', 'dvobject__id')[0:view_limit]

        df_first_created = Datafile.objects.select_related('dvobject'\
                ).filter(Q(checksumvalue='') | Q(checksumvalue__isnull=True),
                ).filter(dvobject__owner_id__in=dataset_ids\
                ).order_by('dvobject__createdate', 'dvobject__id').first()

        df_last_created = Datafile.objects.select_related('dvobject'\
                ).filter(Q(checksumvalue='') | Q(checksumvalue__isnull=True),
                ).filter(dvobject__owner_id__in=dataset_ids\
                ).order_by('-dvobject__createdate', 'dvobject__id').first()

        return (total_cnt, view_limit, dfiles, df_first_created, df_last_created)



    @staticmethod
    def get_basic_stats():

        ds_ids_local = Dataset.objects.filter(harvestingclient__isnull=True\
                                ).values_list('dvobject__id', flat=True)

        cnt_no_checksum_local = Datafile.objects.select_related('dvobject'\
                ).filter(Q(checksumvalue='') | Q(checksumvalue__isnull=True)\
                ).filter(dvobject__owner_id__in=ds_ids_local\
                ).count()

        ds_ids_harvested = Dataset.objects.filter(harvestingclient__isnull=False\
                                ).values_list('dvobject__id', flat=True)

        cnt_no_checksum_harvested = Datafile.objects.select_related('dvobject'\
                ).filter(Q(checksumvalue='') | Q(checksumvalue__isnull=True)\
                ).filter(dvobject__owner_id__in=ds_ids_harvested\
                ).count()


        file_stats = dict(\
            cnt_no_checksum_local=NamedStat(\
                                'No Checksum (Local)',
                                cnt_no_checksum_local,
                                ('Count of Local Datafiles without a checksum'),
                                'view_no_checksum_list_local'),
            cnt_no_checksum_harvested=NamedStat(\
                                'No Checksum (Harvested)',
                                cnt_no_checksum_harvested,
                                ('Count of Harvested Datafiles without a checksum'),
                                'view_no_checksum_list_harvested'),
            )

        return file_stats
