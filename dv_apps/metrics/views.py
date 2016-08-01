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

    # Start an OrderedDict
    resp_dict = OrderedDict()

    # -------------------------
    # Dataverse counts
    # -------------------------
    # Note: For regular use, the success_flag should be checked every time_sort
    #
    success, count_results_or_err = smd.get_dataverse_count()
    if not success:
        return JsonResponse(count_results_or_err)

    dataverse_counts = dict(dataverse_count=count_results_or_err)

    success_flag, dataverse_counts['dataverse_count_published'] = smd.get_dataverse_count_published()
    success_flag, dataverse_counts['dataverse_count_unpublished'] = smd.get_dataverse_count_unpublished()
    resp_dict['dataverse_counts'] = dataverse_counts


    # -------------------------
    # Dataset counts
    # -------------------------
    dataset_counts = {}
    success_flag, dataset_counts['dataset_count'] = smd.get_dataset_count()
    success_flag, dataset_counts['dataset_count_published'] = smd.get_dataset_count_published()
    success_flag, dataset_counts['dataset_count_unpublished'] = smd.get_dataset_count_unpublished()
    resp_dict['dataset_counts'] = dataset_counts


    # -------------------------
    # Datafile counts
    # -------------------------
    datafile_counts = {}
    success_flag, datafile_counts['datafile_count'] = smd.get_datafile_count()
    success_flag, datafile_counts['datafile_count_published'] = smd.get_datafile_count_published()
    success_flag, datafile_counts['datafile_count_unpublished'] = smd.get_datafile_count_unpublished()
    resp_dict['datafile_counts'] = datafile_counts


    # -------------------------
    # Datasets created each month
    # -------------------------
    success, dataset_counts_by_month = smd.get_dataset_counts_by_create_date()
    if success:
        resp_dict['dataset_counts_by_month'] = list(dataset_counts_by_month)

    # -------------------------
    # Datasets published each month
    # -------------------------
    success, datasets_published_counts_by_month = smd.get_dataset_counts_by_publication_date()
    if success:
        resp_dict['datasets_published_counts_by_month'] = list(datasets_published_counts_by_month)

    # -------------------------
    # Datasets modified by month BUT not historical -- only last mod. date shown
    # -------------------------
    success, datasets_modified_counts_by_month = smd.get_dataset_counts_by_modification_date()
    if success:
        resp_dict['datasets_modified_counts_by_month'] = datasets_modified_counts_by_month

    # -------------------------
    # Files downloaded each month
    # -------------------------
    success, file_downloads_by_month = smd.get_downloads_by_month()
    if success:
        resp_dict['file_downloads_by_month'] = list(file_downloads_by_month)

    # -------------------------
    # Dataverses categorized by type
    # -------------------------
    success, dv_counts_by_type = smd.get_dataverse_counts_by_type()
    if success:
        resp_dict['dv_counts_by_type'] = dv_counts_by_type

    # -------------------------
    # Dataverses categorized by affiliation
    # -------------------------
    success, dv_counts_by_affil = smd.get_dataverse_affiliation_counts()
    if success:
        resp_dict['dv_counts_by_affil'] = dv_counts_by_affil

    d = dict(JSON_STATS=json.dumps(resp_dict, indent=4))
    return render(request, 'metrics_api.html', d)

    return HttpResponse('<pre>' + json.dumps(resp_dict, indent=4) + '</pre>')
    return JsonResponse(resp_dict)
