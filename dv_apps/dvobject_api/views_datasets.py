from django.shortcuts import render
from django.http import Http404

from dv_apps.datasets.models import Dataset, DatasetVersion, VERSION_STATE_RELEASED
from dv_apps.datasets.util import get_latest_dataset_version

from dv_apps.dataverses.models import Dataverse
from dv_apps.dataverses.serializer import DataverseSerializer
from django.views.decorators.cache import cache_page

from dv_apps.datasets.serializer import DatasetSerializer


def view_dataset_by_persistent_id(request):

    persistent_id = request.GET.get('persistentId', None)
    if persistent_id is None:
        raise Http404('persistentId not found: %s' % persistent_id)

    ds = Dataset.get_dataset_by_persistent_id(persistent_id)
    if ds is None:
        raise Http404('persistentId not found: %s' % persistent_id)

    dsv = get_latest_dataset_version(ds.dvobject.id)

    if dsv is None:
        raise Http404('dataset_id not found')

    return view_dataset_by_version(request, dsv.id)


def view_single_dataset(request, dataset_id):
    """Dataset view test.  Given dataset id, get latest version"""

    dsv = get_latest_dataset_version(dataset_id)

    if dsv is None:
        raise Http404('dataset_id not found')

    return view_dataset_by_version(request, dsv.id)

"""
http://127.0.0.1:8000/miniverse/dvobjects/api/v1/datasets/by-persistent-id?persistentID=doi:10.7910/DVN/26935

http://127.0.0.1:8000/miniverse/dvobjects/api/v1/datasets/by-id/53121

http://127.0.0.1:8000/miniverse/dvobjects/api/v1/datasets/by-version-id/79678
"""

@cache_page(60 * 60 * 2)
def view_dataset_by_version(request, dataset_version_id):
    """Dataset view test.  Given dataset version id, render HTML"""

    try:
        dsv = DatasetVersion.objects.select_related('dataset')\
            .get(pk=dataset_version_id,
                versionstate=VERSION_STATE_RELEASED)
    except DatasetVersion.DoesNotExist:
        raise Http404

    dataset_dict = DatasetSerializer(dsv).as_json()
    citation_block=dataset_dict.get('metadata_blocks', {}).get('citation')

    dataverse_id = dataset_dict['ownerInfo']['id']
    try:
        dataverse = Dataverse.objects.select_related('dvobject')\
                .get(dvobject__id=dataverse_id)
    except Dataverse.DoesNotExist:
        raise Http404('No Dataverse with id: %s' % dataverse_id)

    dataverse_dict = DataverseSerializer(dataverse).as_json()

    lu = dict(ds=dataset_dict,
            dv=dataverse_dict,
            citation_block=citation_block)

    return render(request, 'dvobject_api/dataset_view.html', lu)
