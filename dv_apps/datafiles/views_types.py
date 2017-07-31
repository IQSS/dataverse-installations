import requests
import os
import StringIO
import simplejson as json
import pandas as pd
from collections import OrderedDict

from django.http import JsonResponse, HttpResponse, Http404
from dv_apps.datafiles.models import Datafile, INGEST_STATUS_NONE

from dv_apps.ingest.mime_type_display import CONTENT_TYPE_TABULAR

from django.conf import settings

from dv_apps.utils import query_helper
from django.views.decorators.cache import cache_page
from dv_apps.utils import query_helper

@cache_page(settings.METRICS_CACHE_VIEW_TIME)
def view_file_content_types(request):
    """JSON list of content types"""

    is_pretty = False
    as_excel = False
    if request.GET.get('as_excel') is not None:
        as_excel = True
    elif request.GET.get('pretty') is not None:
        is_pretty = True


    is_published_param = query_helper.get_is_published_filter_param()

    content_types = Datafile.objects.select_related('dvobject'\
                        ).filter(**is_published_param\
                        ).values_list('contenttype', flat=True\
                        ).distinct().order_by('contenttype')

    d = OrderedDict()
    d['content_types'] = list(content_types)

    if as_excel:
        if len(d) == 0:
            return HttpResponse('nothing found')
        # https://stackoverflow.com/questions/35267585/django-pandas-to-http-response-download-file
        df = pd.read_json(json.dumps(d))
        excel_file = StringIO.StringIO()
        xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
        df.to_excel(xlwriter, 'content_types', index=False)
        xlwriter.save()
        xlwriter.close()
        excel_file.seek(0)
        # set the mime type so that the browser knows what to do with the file
        response = HttpResponse(\
                   excel_file.read(),
                   content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        # set the file name in the Content-Disposition header
        response['Content-Disposition'] = 'attachment; filename=dv_content_types.xlsx'

        return response

    d['description'] = 'Content types of published Dataverse files'

    if is_pretty:
        json_str = '<pre>%s</pre>' % json.dumps(d, indent=4)
        return HttpResponse(json_str)
    else:
        json_str = json.dumps(d)
        return HttpResponse(json_str,
                            content_type="application/json")


@cache_page(settings.METRICS_CACHE_VIEW_TIME)
def view_file_list_by_type(request):
    """Give a list of published files based on the content type.
    e.g.  ?contenttype=text/tab-separated-values
    """
    is_pretty = False
    as_excel = False
    if request.GET.get('as_excel') is not None:
        as_excel = True
    elif request.GET.get('pretty') is not None:
        is_pretty = True

    contenttype = request.GET.get('contenttype', CONTENT_TYPE_TABULAR)

    query_params = dict(contenttype=contenttype,
                        filesize__gt=0,
                        checksumvalue__isnull=False,
                        restricted=False,
                        ingeststatus=INGEST_STATUS_NONE)

    query_params.update(query_helper.get_is_published_filter_param())

    dfiles = Datafile.objects.select_related('dvobject', 'dvobject__owner'\
                    ).filter(**query_params\
                    ).order_by('contenttype')

    flist = [Datafile.to_json(df)\
             for df in dfiles\
             if df is not None and df.id]

    d = OrderedDict()
    d['file_list'] = flist

    if as_excel:
        # https://stackoverflow.com/questions/35267585/django-pandas-to-http-response-download-file
        if len(flist) == 0:
            return HttpResponse('no published files for contenttype: %s' % contenttype)

        df = pd.DataFrame(flist, columns=flist[0].keys())
        excel_file = StringIO.StringIO()
        xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
        df.to_excel(xlwriter, 'file_list', index=False)
        xlwriter.save()
        xlwriter.close()
        excel_file.seek(0)
        # set the mime type so that the browser knows what to do with the file
        response = HttpResponse(\
                   excel_file.read(),
                   content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        # set the file name in the Content-Disposition header
        response['Content-Disposition'] = 'attachment; filename=dv_file_list.xlsx'

        return response

    d['description'] = 'Files with content type %s. Count: %d' % (contenttype, len(flist))

    if is_pretty:
        json_str = '<pre>%s</pre>' % json.dumps(d, indent=4)
        return HttpResponse(json_str)
    else:
        json_str = json.dumps(d)
        return HttpResponse(json_str,
                            content_type="application/json")
