from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.conf import settings
from dv_apps.quality_checks.util_filesize_zero import ZeroFilesizeStats

def view_filesize_zero(request):
    """
    Display stats on files with size zero or null
    """

    info_dict = dict(zstats=ZeroFilesizeStats.get_basic_stats(),
                     hello='over here')

    return render(request,
                  'filesize_zero.html',
                  info_dict)


def view_filesize_zero_local_list(request):
    """
    List local files with size zero or null
    """
    info_dict = dict(dfiles=ZeroFilesizeStats.get_local_files_bad_size(),
                     subtitle='Local files with size zero or null',
                     installation_url=settings.DATAVERSE_INSTALLATION_URL)

    return render(request,
                  'filesize_zero_local_list.html',
                  info_dict)
