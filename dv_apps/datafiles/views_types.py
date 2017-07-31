import requests
import os
import simplejson as json
from collections import OrderedDict

from django.http import JsonResponse, HttpResponse, Http404
from dv_apps.datafiles.models import Datafile

from dv_apps.ingest.mime_type_display import CONTENT_TYPE_TABULAR

from django.conf import settings

from dv_apps.utils import query_helper
from django.views.decorators.cache import cache_page
from dv_apps.utils import query_helper

@cache_page(settings.METRICS_CACHE_VIEW_TIME)
def view_file_content_types(request):
    """JSON list of content types"""

    if request.GET.get('pretty') is not None:
        is_pretty = True
    else:
        is_pretty = False

    is_published_param = query_helper.get_is_published_filter_param()

    content_types = Datafile.objects.select_related('dvobject'\
                        ).filter(**is_published_param\
                        ).values_list('contenttype', flat=True\
                        ).distinct().order_by('contenttype')

    d = OrderedDict()
    d['description'] = 'Content types of published Dataverse files'
    d['content_types'] = list(content_types)

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
    if request.GET.get('pretty') is not None:
        is_pretty = True
    else:
        is_pretty = False

    contenttype = request.GET.get('contenttype', CONTENT_TYPE_TABULAR)

    query_params = dict(contenttype=contenttype,
                        filesize__gt=0,
                        checksumvalue__isnull=False)
    query_params.update(query_helper.get_is_published_filter_param())

    dfiles = Datafile.objects.select_related('dvobject', 'dvobject__owner'\
                    ).filter(**query_params\
                    ).order_by('contenttype')

    flist = [Datafile.to_json(df)\
             for df in dfiles\
             if df is not None and df.id]

    d = OrderedDict()
    d['description'] = 'Files with content type %s. Count: %d' % (contenttype, len(flist))
    d['file_list'] = flist

    print (d)
    if is_pretty:
        json_str = '<pre>%s</pre>' % json.dumps(d, indent=4)
        return HttpResponse(json_str)
    else:
        json_str = json.dumps(d)
        return HttpResponse(json_str,
                            content_type="application/json")
