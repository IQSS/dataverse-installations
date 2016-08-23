import json
from collections import OrderedDict

from django.shortcuts import render
from django.http import Http404

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.forms.models import model_to_dict
from django.views.decorators.cache import cache_page

from django.core import serializers

from dv_apps.datasets.models import Dataset, DatasetVersion
from dv_apps.datasets.util import DatasetUtil

def get_pretty_val(request):
    """Quick check of url param to pretty print JSON"""

    if request.GET.get('pretty', None) is not None:
        return True
    return False


#@cache_page(60 * 60 * 2)
def view_single_dataset_by_id(request, dataset_version_id):

    try:
        dataset_version = DatasetVersion.objects.select_related('dataset'\
            ).get(pk=dataset_version_id)
    except DatasetVersion.DoesNotExist:
        raise Http404

    return view_single_dataset_version(request, dataset_version)


@cache_page(60 * 15)
def view_single_dataset_version(request, dsv):
    """
    Show JSON for a single DatasetVersion
    """
    if dsv is None:
        raise Http404

    assert isinstance(dsv, DatasetVersion), "dv must be a DatasetVersion object or None"

    is_pretty = request.GET.get('pretty', None)
    if is_pretty is not None:
        is_pretty = True

    resp_dict = OrderedDict()
    resp_dict['status'] = "OK"
    resp_dict['data'] = DatasetUtil(dsv).as_json()
    #model_to_dict(dv)

    if is_pretty:
        s = '<pre>%s</pre>' % json.dumps(resp_dict, indent=4)
        return HttpResponse(s)
    else:
        return JsonResponse(resp_dict)#, content_type='application/json')
