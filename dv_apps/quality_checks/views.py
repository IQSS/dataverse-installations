from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.conf import settings
from dv_apps.quality_checks.util_filesize_zero import ZeroFilesizeStats
from dv_apps.quality_checks.util_no_checksum import NoChecksumStats
from dv_apps.quality_checks.util_notifications import NotificationStats
from dv_apps.quality_checks.util_content_types import ContentTypeStats
from dv_apps.quality_checks.util_failed_ingest import FailedIngestStats,\
    EXCLUDE_FILESIZE_PARAM
from django.views.decorators.cache import cache_page
from dv_apps.datafiles.models import\
        INGEST_STATUS_INPROGRESS, INGEST_STATUS_ERROR,\
        INGEST_STATUS_NONE, INGEST_STATUS_SCHEDULED

#from django.contrib.auth.decorators import login_required

def add_ingest_status_lookup(template_dict):
    """Add ingest lookup items"""
    template_dict['INGEST_STATUS_NONE'] = INGEST_STATUS_NONE
    template_dict['INGEST_STATUS_SCHEDULED'] = INGEST_STATUS_SCHEDULED
    template_dict['INGEST_STATUS_INPROGRESS'] = INGEST_STATUS_INPROGRESS
    template_dict['INGEST_STATUS_ERROR'] = INGEST_STATUS_ERROR


@cache_page(settings.METRICS_CACHE_VIEW_TIME)
def view_qc_dashboard(request):
    """
    Display QC dashboard (beginning, only 3 simple measures right now)
    """

    info_dict = dict(\
            size_zero_stats=ZeroFilesizeStats.get_basic_stats(),
            checksum_stats=NoChecksumStats.get_basic_stats(),
            notification_stats=NotificationStats.get_basic_stats(),
            unknown_ctype_stats=ContentTypeStats.get_basic_stats(),
            ingest_stats=FailedIngestStats.get_basic_stats())

    return render(request,
                  'qc_dashboard.html',
                  info_dict)


#@login_required
def view_filesize_zero_local_list(request):
    """
    List local files with size zero or null
    """
    dfiles, df_first_created, df_last_created = ZeroFilesizeStats.get_local_files_bad_size()
    dataset_ids = list(set([df.dvobject.owner_id for df in dfiles]))
    num_datasets = len(dataset_ids)

    info_dict = dict(dfiles=dfiles,
                     df_first_created=df_first_created,
                     df_last_created=df_last_created,
                    num_datasets=num_datasets,
                     subtitle='Local files with size zero or null',
                     installation_url=settings.DATAVERSE_INSTALLATION_URL)

    add_ingest_status_lookup(info_dict)

    return render(request,
                  'filesize_zero_local_list.html',
                  info_dict)


def view_in_progress_ingest_list(request):
    dfiles, df_first_created, df_last_created = FailedIngestStats.get_files_in_progress_ingest()
    dataset_ids = list(set([df.dvobject.owner_id for df in dfiles]))
    num_datasets = len(dataset_ids)

    info_dict = dict(dfiles=dfiles,
                     df_first_created=df_first_created,
                     df_last_created=df_last_created,
                     num_datasets=num_datasets,
                     subtitle='Files with an ingest status of "ERROR"',
                     installation_url=settings.DATAVERSE_INSTALLATION_URL,
                     )

    add_ingest_status_lookup(info_dict)

    return render(request,
                  'filesize_zero_local_list.html',
                  info_dict)

def view_bad_ingest_list(request):
    """List of files with ingest error status"""

    kwargs = {}
    if request.GET.has_key(EXCLUDE_FILESIZE_PARAM):
        kwargs[EXCLUDE_FILESIZE_PARAM] = request.GET[EXCLUDE_FILESIZE_PARAM]

    dfiles, df_first_created, df_last_created, num_datasets, num_dataverses =\
        FailedIngestStats.get_files_bad_ingest(**kwargs)

    #dataset_ids = list(set([df.dvobject.owner_id for df in dfiles]))
    #num_datasets = len(dataset_ids)

    info_dict = dict(dfiles=dfiles,
                     df_first_created=df_first_created,
                     df_last_created=df_last_created,
                     num_datasets=num_datasets,
                     num_dataverses=num_dataverses,
                     subtitle='Files with an ingest status of "ERROR"',
                     installation_url=settings.DATAVERSE_INSTALLATION_URL,
                     )

    add_ingest_status_lookup(info_dict)

    return render(request,
                  'filesize_zero_local_list.html',
                  info_dict)


#@login_required
def view_no_checksum_list_harvested(request):
    """Return list of Harvested files w/o a checksum"""
    return view_no_checksum_list(request, harvested_only=True)

#@login_required
def view_no_checksum_list(request, harvested_only=False):
    """
    List of all files with no checksum
     - Defaults to Local files only
     - harvested_only flag will give a list of harveted files
    """
    if harvested_only:
        subtitle = 'Harvested Files without Checksum values'
    else:
        subtitle = 'Local Files without Checksum values'

    total_cnt, view_limit, dfiles, df_first_created, df_last_created = NoChecksumStats.get_files_no_checksum(harvested_only)


    dataset_ids = list(set([df.dvobject.owner_id for df in dfiles]))
    num_datasets = len(dataset_ids)

    subtitle = 'Files without Checksum values'

    info_dict = dict(dfiles=dfiles,
                     total_cnt=total_cnt,
                     view_limit=view_limit,
                     df_first_created=df_first_created,
                     df_last_created=df_last_created,
                     num_datasets=num_datasets,
                     subtitle=subtitle,
                     installation_url=settings.DATAVERSE_INSTALLATION_URL)

    add_ingest_status_lookup(info_dict)

    return render(request,
                  'filesize_zero_local_list.html',
                  info_dict)
