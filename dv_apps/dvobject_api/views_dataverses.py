import json
from collections import OrderedDict

from django.http import Http404
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import cache_page


from dv_apps.dataverses.models import Dataverse
from dv_apps.dataverses.util import DataverseUtil

def get_pretty_val(request):
    """Quick check of url param to pretty print JSON"""

    if request.GET.get('pretty', None) is not None:
        return True
    return False

@cache_page(60 * 60 * 2)
@login_required
def view_single_dataverse_by_alias(request, alias):

    try:
        dv = Dataverse.objects.select_related('dvobject').get(alias=alias)
    except Dataverse.DoesNotExist:
        raise Http404

    return view_single_dataverse(request, dv)

@cache_page(60 * 60 * 2)
@login_required
def view_single_dataverse_by_id(request, dataverse_id):

    try:
        dv = Dataverse.objects.select_related('dvobject').get(dvobject__id =dataverse_id)
    except Dataverse.DoesNotExist:
        raise Http404

    return view_single_dataverse(request, dv)


@cache_page(60 * 15)
@login_required
def view_single_dataverse(request, dv):
    """
    Show JSON for a single Dataverse
    """
    if dv is None:
        raise Http404

    assert isinstance(dv, Dataverse), "dv must be a Dataverse object or None"

    is_pretty = request.GET.get('pretty', None)
    if is_pretty is not None:
        is_pretty = True

    resp_dict = OrderedDict()
    resp_dict['status'] = "OK"
    resp_dict['data'] = DataverseUtil(dv).as_json()
    #model_to_dict(dv)

    if is_pretty:
        s = '<pre>%s</pre>' % json.dumps(resp_dict, indent=4)
        return HttpResponse(s)
    else:
        return JsonResponse(resp_dict)#, content_type='application/json')
