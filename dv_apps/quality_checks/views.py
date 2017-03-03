from django.shortcuts import render
from django.http import HttpResponse, Http404

from dv_apps.quality_checks.util_filesize_zero import ZeroFilesizeStats

def view_filesize_zero(request):
    """
    Display stats on files with size zero or null
    """

    info_dict = dict(zstats=ZeroFilesizeStats.get_basic_stats(),
                     hello='over here')
    #print 'info_dict', info_dict.keys()
    #for dkey, dval in info_dict.items():
    #    print dval.name, dval.stat



    return render(request,
                  'filesize_zero.html',
                  info_dict)
    return HttpResponse('view_filesize_zero')
