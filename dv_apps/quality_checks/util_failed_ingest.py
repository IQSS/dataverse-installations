"""
Checks for filesizes with zero or null

Expected:
    Local files:with size zero
      - No local files with size null
      -
           No harvested files size zero


"""
from django.db.models import Q

from collections import OrderedDict

from dv_apps.datasets.models import Dataset, DatasetVersion
from dv_apps.datafiles.models import Datafile, FileMetadata,\
        INGEST_STATUS_INPROGRESS, INGEST_STATUS_ERROR,\
        INGEST_STATUS_NONE, INGEST_STATUS_SCHEDULED
from dv_apps.quality_checks.named_stat import NamedStat
from dv_apps.datafiles.models import FileMetadata

class FailedIngestStats(object):

    def __init__(self):
        pass

    """
    @staticmethod
    def get_file_metadata_info(datafile_filters):

        dfiles_formatted = []


        dfile_ids = Datafile.objects.select_related('dvobject'\
                        ).filter(**datafile_filters\
                        ).values_list('dvobject__id', flat=True)

        file_metadatas = FileMetadata.objects.filter(\
                datafile__id__in=dfile_ids\
                ).orderby('datafile__id', '-version')

        for fm in


        dfile_ids = [ df.dvobject.id for df in dfiles]

        FileMetadata

        for df in dfil
    """
    @staticmethod
    def get_files_in_progress_ingest():
        """List of fails with ingest status IN PROGRESS"""

        dfiles = Datafile.objects.select_related('dvobject'\
                ).filter(ingeststatus=INGEST_STATUS_INPROGRESS\
                ).order_by('dvobject__owner_id', 'dvobject__id')

        df_first_created = Datafile.objects.select_related('dvobject'\
                ).filter(ingeststatus=INGEST_STATUS_INPROGRESS\
                ).order_by('dvobject__createdate', 'dvobject__id').first()

        df_last_created = Datafile.objects.select_related('dvobject'\
                ).filter(ingeststatus=INGEST_STATUS_INPROGRESS\
                ).order_by('-dvobject__createdate', 'dvobject__id').first()

        return (dfiles, df_first_created, df_last_created)

    @staticmethod
    def get_filesize_exclude_param():

        return dict(filesize=1226912)

    @staticmethod
    def get_files_bad_ingest():
        """List of fails with ingest status ERROR"""

        dfiles = Datafile.objects.select_related('dvobject'\
                ).filter(ingeststatus=INGEST_STATUS_ERROR\
                ).exclude(**FailedIngestStats.get_filesize_exclude_param()\
                ).order_by('dvobject__owner_id', 'dvobject__id')

        df_first_created = Datafile.objects.select_related('dvobject'\
                ).filter(ingeststatus=INGEST_STATUS_ERROR\
                ).exclude(**FailedIngestStats.get_filesize_exclude_param()\
                ).order_by('dvobject__createdate', 'dvobject__id').first()

        df_last_created = Datafile.objects.select_related('dvobject'\
                ).filter(ingeststatus=INGEST_STATUS_ERROR\
                ).exclude(**FailedIngestStats.get_filesize_exclude_param()\
                ).order_by('-dvobject__createdate', 'dvobject__id').first()

        return (dfiles, df_first_created, df_last_created)


    @staticmethod
    def dataset_contacts():

        # unique dataset ids
        ds_ids_ingest_error = Datafile.objects.select_related('dvobject'\
                            ).filter(ingeststatus=INGEST_STATUS_ERROR\
                            ).exclude(**FailedIngestStats.get_filesize_exclude_param()\
                            ).values_list('dvobject__owner_id', flat=True\
                            ).distinct().order_by()

        # how to get dataset titles/contacts easily w/o solr?
        """
from dv_apps.datafiles.models import Datafile
from dv_apps.dataverses.models import Dataverse
from dv_apps.datasets.models import Dataset
from dv_apps.datasetfields.utils import get_dataset_title



ds_ids_ingest_error = Datafile.objects.select_related('dvobject'\
                    ).filter(ingeststatus=INGEST_STATUS_ERROR\
                    ).exclude(filesize=1226912\
                    ).values_list('dvobject__owner_id', flat=True\
                    ).distinct().order_by()

dv_ids = Dataset.objects.select_related('dvobject'\
                    ).filter(dvobject__id__in=ds_ids_ingest_error\
                    ).values_list('dvobject__owner_id', flat=True\
                    ).distinct().order_by()


len(dv_ids)

dvs = Dataverse.objects.select_related('dvobject'
                    ).filter(dvobject__id__in=dv_ids)

for dv in dvs:
    print '%s (%s)' % (dv.name, dv.affiliation)
#, dv.description

        """

    @staticmethod
    def get_basic_stats():

        cnt_ingest_error = Datafile.objects.filter(\
                            ingeststatus=INGEST_STATUS_ERROR
                            ).exclude(filesize=1226912\
                            ).count()

        cnt_ingest_in_progress = Datafile.objects.filter(\
                            ingeststatus=INGEST_STATUS_INPROGRESS).count()


        file_stats = dict(\
            cnt_ingest_error=NamedStat(\
                                'Ingest Errors',
                                cnt_ingest_error,
                                ('Count of Datafiles with'
                                 ' an ingest status of "Error."'
                                 ' (These files should have'
                                 ' been converted to tabular files.)'),
                                'view_bad_ingest_list'),
            cnt_ingest_in_progress=NamedStat(\
                                'Ingest In Progress',
                                cnt_ingest_in_progress,
                                ('Count of Datafiles with'
                                 ' an ingest status of "In Progress."'
                                 '(These files may be "stuck" at ingest)'),
                                'view_in_progress_ingest_list'),
            #cnt_harvested_zero=NamedStat(\
            #                    'Filesize 0 (Harvested)',
            #                    cnt_harvested_zero,
            #                    ('Count of harvested Datafiles displaying a'
            #                     ' size of 0 bytes')),
            )

        return file_stats
