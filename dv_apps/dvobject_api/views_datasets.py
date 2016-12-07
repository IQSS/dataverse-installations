import json
from collections import OrderedDict

from django.shortcuts import render, render_to_response
from django.http import Http404
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse, HttpResponse
from dv_apps.datasets.models import Dataset, DatasetVersion
from django.views.decorators.cache import cache_page


from dv_apps.datasets.util import DatasetUtil

def get_pretty_val(request):
    """Quick check of url param to pretty print JSON"""

    if request.GET.get('pretty', None) is not None:
        return True
    return False


def view_single_dataset(request, dataset_id):

    try:
        dataset = Dataset.objects.get(pk=dataset_id)
    except Dataset.DoesNotExist:
        return Http404('dataset_id not found')


    dataset_version = DatasetVersion.objects\
                    .select_related('dataset'\
                    ).filter(dataset=dataset)\
                    .values('id')\
                    .order_by('-id').first()

    if not dataset_version:
        return Http404('dataset_version not found')


    return view_single_dataset_by_id(request, dataset_version.get('id', None))


#@cache_page(60 * 60 * 2)
@login_required
def view_single_dataset_by_id(request, dataset_version_id):

    try:
        dataset_version = DatasetVersion.objects.select_related('dataset'\
            ).get(pk=dataset_version_id)
    except DatasetVersion.DoesNotExist:
        raise Http404

    return view_single_dataset_version(request, dataset_version)

@login_required
@cache_page(60 * 60 * 2)
def view_single_dataset_test_view(request, dataset_version_id):

    try:
        dsv = DatasetVersion.objects.select_related('dataset'\
            ).get(pk=dataset_version_id)
    except DatasetVersion.DoesNotExist:
        raise Http404

    dataset_dict = DatasetUtil(dsv).as_json()
    citation_block=dataset_dict.get('metadata_blocks', {}).get('citation')

    lu = dict(ds=dataset_dict,
            citation_block=citation_block
            )

    return render(request, 'dvobject_api/test.html', lu)


#@cache_page(60 * 15)
@login_required
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
