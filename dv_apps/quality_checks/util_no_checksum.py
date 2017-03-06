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
    def get_files_no_checksum():
        """Return a list of Datafile objects missing the checksum"""

        dfiles = Datafile.objects.select_related('dvobject'\
                ).filter(Q(checksumvalue='') | Q(checksumvalue__isnull=True),
                ).order_by('dvobject__owner_id', 'dvobject__id')

        return dfiles



    @staticmethod
    def get_basic_stats():

        cnt_no_checksum = Datafile.objects.select_related('dvobject'\
                ).filter(Q(checksumvalue='') | Q(checksumvalue__isnull=True),
                ).count()


        file_stats = dict(\
            cnt_no_checksum=NamedStat(\
                                'No Checksum',
                                cnt_no_checksum,
                                ('Count of Datafiles without a checksum'),
                                'view_no_checksum_list'),
            )

        return file_stats
