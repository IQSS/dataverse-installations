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
    stats_dv_count = stats_dvs.get_dataverse_count()
    if stats_dv_count.has_error():
        return JsonResponse(dict(error_message=stats_dv_count.error_message))

    dataverse_counts = dict(dataverse_count=stats_dv_count.result_data)

    stats_dv_count_published = stats_dvs.get_dataverse_count_published()
    if not stats_dv_count_published.has_error():
        dataverse_counts['dataverse_count_published'] = stats_dv_count_published.result_data

    stats_dv_count_unpublished = stats_dvs.get_dataverse_count_unpublished()
    if not stats_dv_count_unpublished.has_error():
        dataverse_counts['dataverse_count_unpublished'] = stats_dv_count_unpublished.result_data

    resp_dict['dataverse_counts'] = dataverse_counts


    # -------------------------
    # Dataset counts
    # -------------------------
    dataset_counts = {}
    stats_ds_count = stats_datasets.get_dataset_count()
    if stats_ds_count.was_succcess():
        dataset_counts['dataset_count'] = stats_ds_count.result_data

    stats_ds_count_published = stats_datasets.get_dataset_count_published()
    if stats_ds_count_published.was_succcess():
        dataset_counts['dataset_count_published'] = stats_ds_count_published.result_data

    stats_ds_count_unpublished = stats_datasets.get_dataset_count_unpublished()
    if stats_ds_count_unpublished.was_succcess():
        dataset_counts['dataset_count_unpublished'] = stats_ds_count_unpublished.result_data

    resp_dict['dataset_counts'] = dataset_counts


    # -------------------------
    # Datafile counts
    # -------------------------
    datafile_counts = {}
    stats_file_count = stats_files.get_datafile_count()
    if stats_file_count.was_succcess():
        datafile_counts['datafile_count'] = stats_file_count.result_data

    stats_file_count_published = stats_files.get_datafile_count_published()
    if stats_file_count_published.was_succcess():
        datafile_counts['datafile_count_published'] = stats_file_count_published.result_data

    stats_file_count_unpublished = stats_files.get_datafile_count_unpublished()
    if stats_file_count_unpublished.was_succcess():
        datafile_counts['datafile_count_unpublished'] = stats_file_count_unpublished.result_data


    # -------------------------
    # Dataverses created each month
    # -------------------------
    dataverse_counts_by_month = stats_dvs.get_dataverse_counts_by_month()
    if not dataverse_counts_by_month.has_error():
        resp_dict['dataverse_counts_by_month'] = list(dataverse_counts_by_month.result_data)

    # -------------------------
    # Datasets created each month
    # -------------------------
    dataset_counts_by_month = stats_datasets.get_dataset_counts_by_create_date()
    if not dataset_counts_by_month.has_error():
        resp_dict['dataset_counts_by_month'] = list(dataset_counts_by_month.result_data)

    # -------------------------
    # Datasets published each month
    # -------------------------
    datasets_published_counts_by_month = stats_datasets.get_dataset_counts_by_publication_date()
    if not datasets_published_counts_by_month.has_error():
        resp_dict['datasets_published_counts_by_month'] =\
         list(datasets_published_counts_by_month.result_data)

    # -------------------------
    # Datasets modified by month BUT not historical -- only last mod. date shown
    # -------------------------
    datasets_modified_counts_by_month = stats_datasets.get_dataset_counts_by_modification_date()
    if not datasets_modified_counts_by_month.has_error():
        resp_dict['datasets_modified_counts_by_month'] = datasets_modified_counts_by_month.result_data

    # -------------------------
    # Files downloaded each month
    # -------------------------
    file_downloads_by_month = stats_files.get_file_downloads_by_month_published()
    if not file_downloads_by_month.has_error():
        resp_dict['file_downloads_by_month'] = list(file_downloads_by_month.result_data)

    # -------------------------
    # Datafiles by content type
    # -------------------------
    datafile_content_type_counts = stats_files.get_datafile_content_type_counts()
    if not datafile_content_type_counts.has_error():
        resp_dict['datafile_content_type_counts'] = datafile_content_type_counts.result_data


    # -------------------------
    # Dataverses categorized by type
    # -------------------------
    dv_counts_by_type = stats_dvs.get_dataverse_counts_by_type()
    if not dv_counts_by_type.has_error():
        resp_dict['dv_counts_by_type'] = dv_counts_by_type.result_data

    # -------------------------
    # Dataverses categorized by affiliation
    # -------------------------
    dv_counts_by_affiliation = stats_dvs.get_dataverse_affiliation_counts()
    if not dv_counts_by_affiliation.has_error():
        resp_dict['dv_counts_by_affiliation'] = dv_counts_by_affiliation.result_data

    d = dict(JSON_STATS=json.dumps(resp_dict, indent=4))
    return render(request, 'metrics_api.html', d)

    return HttpResponse('<pre>' + json.dumps(resp_dict, indent=4) + '</pre>')
    return JsonResponse(resp_dict)
