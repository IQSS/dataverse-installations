from django.shortcuts import render
from django.http import Http404

from dv_apps.datasets.models import DatasetVersion, VERSION_STATE_RELEASED
from dv_apps.datasets.util import get_latest_dataset_version

from dv_apps.dataverses.models import Dataverse
from dv_apps.dataverses.serializer import DataverseSerializer
from django.views.decorators.cache import cache_page

from dv_apps.datasets.serializer import DatasetSerializer


def view_single_dataset_test_view(request, dataset_id):
    """Dataset view test.  Given dataset id, get latest version"""
    
    dsv = get_latest_dataset_version(dataset_id)

    if dsv is None:
        raise Http404('dataset_id not found')

    return view_single_datasetversion_test_view(request, dsv.id)

@cache_page(60 * 60 * 2)
def view_single_datasetversion_test_view(request, dataset_version_id):
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
