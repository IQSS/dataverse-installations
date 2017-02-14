"""View Differences between two Datasets"""
import json

from django.shortcuts import render
from django.http import HttpResponse, Http404
#from django.contrib.auth.decorators import login_required

from dv_apps.datasets.models import Dataset, DatasetVersion
from dv_apps.datasetfields.utils import get_dataset_title
from dv_apps.datasetfields.models import DatasetField, DatasetFieldValue, DatasetFieldType
from dv_apps.datasetfields.metadata_formatter import MetadataFormatter
from dv_apps.datasets.serializer import DatasetSerializer

from dv_apps.datasets.dataset_differences import DatasetDifferences

def view_differences(request, dataset_id):
    """View differences between two datasets"""
    try:
        dataset = Dataset.objects.get(pk=dataset_id)
    except Dataset.DoesNotExist:
        raise Http404('dataset_id not found')


    dataset_versions = DatasetVersion.objects.select_related('dataset'\
                    ).filter(dataset=dataset)

    lookup = dict(dataset=dataset,\
                 dataset_versions=dataset_versions)

    if dataset_versions.count() < 2:
        return HttpResponse("Only one version of this dataset")

    # -----------------------------
    # Retrieve two dataset versions and create JSON docs
    # -----------------------------
    latest_version = dataset_versions[0]
    previous_version = dataset_versions[1]

    latest_json = DatasetSerializer(latest_version).as_json()
    latest_json_string = json.dumps(latest_json, indent=4)

    previous_json = DatasetSerializer(previous_version).as_json()
    previous_json_string = json.dumps(previous_json, indent=4)

    # -----------------------------
    # compare JSON docs
    # -----------------------------
    ds_diffs = DatasetDifferences(latest_json, previous_json)
    ds_diffs.run_comparison()
    ds_diffs.show_diffs()


    # -----------------------------
    # format attributes for template
    # -----------------------------
    lookup = dict(\
                dataset=dataset,
                latest_json=latest_json_string,
                previous_json=previous_json_string,
                diff_list=ds_diffs.get_diffferences())


    return render(request, 'view_differences.html', lookup)
