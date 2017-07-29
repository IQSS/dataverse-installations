import json
from collections import OrderedDict

from dv_apps.utils import query_helper

from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import cache_page

from dv_apps.dataverses.models import Dataverse
from dv_apps.dataverses.serializer import DataverseSerializer

from django.conf import settings

def get_pretty_val(request):
    """Quick check of url param to pretty print JSON"""

    if request.GET.get('pretty', None) is not None:
        return True
    return False

@cache_page(60 * 60 * 2)
def view_single_dataverse_by_alias(request, alias):
    """JSON repr. of Dataverse. Published Dataverses only"""
    query_params = dict(alias=alias)
    query_params.update(query_helper.get_is_published_filter_param())

    try:
        dv = Dataverse.objects.select_related('dvobject').get(**query_params)
    except Dataverse.DoesNotExist:
        raise Http404

    return _view_single_dataverse(request, dv)

#@login_required
@cache_page(60 * 60 * 2)
def view_single_dataverse_by_id(request, dataverse_id):
    """JSON repr. of Dataverse. Published Dataverses only"""

    query_params = dict(dvobject__id=dataverse_id)
    query_params.update(query_helper.get_is_published_filter_param())

    try:
        dv = Dataverse.objects.select_related('dvobject').get(**query_params)
    except Dataverse.DoesNotExist:
        raise Http404

    return _view_single_dataverse(request, dv)


def view_get_slack_dataverse_info(dataverse_id):

    try:
        dv = Dataverse.objects.select_related('dvobject'\
                        ).get(dvobject__id=dataverse_id)
    except Dataverse.DoesNotExist:
        return "Sorry, no Dataverse found for id: %s" % dataverse_id

    dv_dict = DataverseSerializer(dv).as_json()

    #ref_url = reverse('view_single_dataverse_by_id', kwargs=dict(dataverse_id=dataverse_id))

    ref_url = '%s/dataverse.xhtml?Id=%s' % (settings.DATAVERSE_INSTALLATION_URL, dataverse_id)

    return """```%s```\nreference: %s""" %\
        (json.dumps(dv_dict, indent=4), ref_url)


#@login_required
@cache_page(60 * 15)
def _view_single_dataverse(request, dv):
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
    resp_dict['data'] = DataverseSerializer(dv).as_json()
    #model_to_dict(dv)

    if is_pretty:
        s = '<pre>%s</pre>' % json.dumps(resp_dict, indent=4)
        return HttpResponse(s)
    else:
        return JsonResponse(resp_dict)#, content_type='application/json')
