"""
Metric views, returning JSON repsonses
"""

from collections import OrderedDict
import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import cache_page

from dv_apps.metrics.stats_util_datasets import StatsMakerDatasets


#@cache_page(60 * 6)
def view_simple_dataset_count2(request):
    """Stripped down example"""

    smd = StatsMakerDatasets(**request.GET.dict())

    success, dataset_count = smd.get_dataset_count()

    if not success:
        return JsonResponse(smd.get_http_error_dict(), status=smd.get_http_err_code())

    resp_dict = OrderedDict({'dataset_count' : dataset_count})

    """
    success, combined_counts = smd.get_dataset_counts_by_create_date_and_pub_date()
    if success:
        resp_dict['combined_counts'] = list(combined_counts)
    """

    success, dataverse_count = smd.get_dataverse_count()
    if success:
        resp_dict['dataverse_count'] = dataverse_count

    success, dataset_count = smd.get_dataset_count()
    if success:
        resp_dict['dataset_count'] = dataset_count

    success, datafile_count = smd.get_datafile_count()
    if success:
        resp_dict['datafile_count'] = datafile_count


    success, dataset_counts_by_month = smd.get_dataset_counts_by_create_date()
    if success:
        resp_dict['dataset_counts_by_month'] = list(dataset_counts_by_month)

    success, datasets_published_counts_by_month = smd.get_dataset_counts_by_publication_date()
    if success:
        resp_dict['datasets_published_counts_by_month'] = list(datasets_published_counts_by_month)

    success, datasets_modified_counts_by_month = smd.get_dataset_counts_by_modification_date()
    if success:
        resp_dict['datasets_modified_counts_by_month'] = datasets_modified_counts_by_month

    success, file_downloads_by_month = smd.get_downloads_by_month()
    if success:
        resp_dict['file_downloads_by_month'] = list(file_downloads_by_month)

    success, dv_counts_by_type = smd.get_dataverse_counts_by_type()
    if success:
        resp_dict['dv_counts_by_type'] = dv_counts_by_type

    success, dv_counts_by_affil = smd.get_dataverse_affiliation_counts()
    if success:
        resp_dict['dv_counts_by_affil'] = dv_counts_by_affil

    d = dict(JSON_STATS=json.dumps(resp_dict, indent=4))
    return render(request, 'metrics_api.html', d)

    return HttpResponse('<pre>' + json.dumps(resp_dict, indent=4) + '</pre>')
    return JsonResponse(resp_dict)
