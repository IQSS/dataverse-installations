"""
Metric views, returning JSON repsonses
"""

from collections import OrderedDict
import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import cache_page
from dv_apps.metrics.stats_util_datasets import StatsMakerDatasets
from dv_apps.metrics.stats_util_dataverses import StatsMakerDataverses
from dv_apps.metrics.stats_util_files import StatsMakerFiles

from dv_apps.metrics.stats_util_datasets import StatsMakerDatasets


#@cache_page(60 * 6)
def view_simple_dataset_count2(request):
    """Stripped down example"""

    #smd = StatsMakerDatasets(**request.GET.dict())
    stats_dvs = StatsMakerDataverses(**request.GET.dict())
    stats_datasets = StatsMakerDatasets(**request.GET.dict())
    stats_files = StatsMakerFiles(**request.GET.dict())

    # Start an OrderedDict
    resp_dict = OrderedDict()

    # -------------------------
    # Dataverse counts
    # -------------------------
    # Note: For regular use, the success_flag should be checked every time_sort
    #
    success, count_results_or_err = stats_dvs.get_dataverse_count()
    if not success:
        return JsonResponse(count_results_or_err)

    dataverse_counts = dict(dataverse_count=count_results_or_err)

    success_flag, dataverse_counts['dataverse_count_published'] = stats_dvs.get_dataverse_count_published()
    success_flag, dataverse_counts['dataverse_count_unpublished'] = stats_dvs.get_dataverse_count_unpublished()
    resp_dict['dataverse_counts'] = dataverse_counts


    # -------------------------
    # Dataset counts
    # -------------------------
    dataset_counts = {}
    success_flag, dataset_counts['dataset_count'] = stats_datasets.get_dataset_count()
    success_flag, dataset_counts['dataset_count_published'] = stats_datasets.get_dataset_count_published()
    success_flag, dataset_counts['dataset_count_unpublished'] = stats_datasets.get_dataset_count_unpublished()
    resp_dict['dataset_counts'] = dataset_counts


    # -------------------------
    # Datafile counts
    # -------------------------
    datafile_counts = {}
    success_flag, datafile_counts['datafile_count'] = stats_files.get_datafile_count()
    success_flag, datafile_counts['datafile_count_published'] = stats_files.get_datafile_count_published()
    success_flag, datafile_counts['datafile_count_unpublished'] = stats_files.get_datafile_count_unpublished()
    resp_dict['datafile_counts'] = datafile_counts


    # -------------------------
    # Datafiles by content type
    # -------------------------
    #success, number_of_datafile_types = smd.get_number_of_datafile_types()
    #if success:
    #    resp_dict['number_of_datafile_types'] = list(number_of_datafile_types)

    success, datafile_content_type_counts = stats_files.get_datafile_content_type_counts()
    if success:
        resp_dict['datafile_content_type_counts'] = datafile_content_type_counts


    # -------------------------
    # Dataverses created each month
    # -------------------------
    success, dataverse_counts_by_month = stats_dvs.get_dataverse_counts_by_month()
    if success:
        resp_dict['dataverse_counts_by_month'] = list(dataverse_counts_by_month)


    # -------------------------
    # Datasets created each month
    # -------------------------
    success, dataset_counts_by_month = stats_datasets.get_dataset_counts_by_create_date()
    if success:
        resp_dict['dataset_counts_by_month'] = list(dataset_counts_by_month)

    # -------------------------
    # Datasets published each month
    # -------------------------
    success, datasets_published_counts_by_month = stats_datasets.get_dataset_counts_by_publication_date()
    if success:
        resp_dict['datasets_published_counts_by_month'] = list(datasets_published_counts_by_month)

    # -------------------------
    # Datasets modified by month BUT not historical -- only last mod. date shown
    # -------------------------
    success, datasets_modified_counts_by_month = stats_datasets.get_dataset_counts_by_modification_date()
    if success:
        resp_dict['datasets_modified_counts_by_month'] = datasets_modified_counts_by_month

    # -------------------------
    # Files downloaded each month
    # -------------------------
    success, file_downloads_by_month = stats_files.get_file_downloads_by_month_published()
    if success:
        resp_dict['file_downloads_by_month'] = list(file_downloads_by_month)

    # -------------------------
    # Dataverses categorized by type
    # -------------------------
    success, dv_counts_by_type = stats_dvs.get_dataverse_counts_by_type()
    if success:
        resp_dict['dv_counts_by_type'] = dv_counts_by_type

    # -------------------------
    # Dataverses categorized by affiliation
    # -------------------------
    success, dv_counts_by_affiliation = stats_dvs.get_dataverse_affiliation_counts()
    if success:
        resp_dict['dv_counts_by_affiliation'] = dv_counts_by_affiliation

    d = dict(JSON_STATS=json.dumps(resp_dict, indent=4))
    return render(request, 'metrics_api.html', d)

    return HttpResponse('<pre>' + json.dumps(resp_dict, indent=4) + '</pre>')
    return JsonResponse(resp_dict)
