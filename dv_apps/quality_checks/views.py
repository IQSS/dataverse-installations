from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.conf import settings
from dv_apps.quality_checks.util_filesize_zero import ZeroFilesizeStats
from dv_apps.quality_checks.util_no_checksum import NoChecksumStats
from django.contrib.auth.decorators import login_required

#@login_required
def view_qc_dashboard(request):
    """
    Display QC dashboard (beginning, only 3 simple measures right now)
    """

    info_dict = dict(size_zero_stats=ZeroFilesizeStats.get_basic_stats(),
                     checksum_stats=NoChecksumStats.get_basic_stats())

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

    return render(request,
                  'filesize_zero_local_list.html',
                  info_dict)
