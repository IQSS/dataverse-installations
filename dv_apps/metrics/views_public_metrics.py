"""
Metric views, returning JSON repsonses
"""
from collections import OrderedDict
import json
from os.path import splitext
from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import cache_page
from django.http import JsonResponse, HttpResponse, Http404

from dv_apps.datafiles.models import Datafile, FileMetadata
from dv_apps.metrics.stats_util_datasets import StatsMakerDatasets
from dv_apps.metrics.stats_util_dataverses import StatsMakerDataverses
from dv_apps.metrics.stats_util_files import StatsMakerFiles

ONE_HOUR_IN_SECONDS = 60 * 60 * 1
TWO_HOURS_IN_SECONDS = 60 * 60 * 2

#@cache_page(TWO_HOURS_IN_SECONDS)
def view_public_visualizations_last12(request):
    """
    Return visualizations covering the last 12 months+.

    e.g. If it's July 23, 2016, it will start from July 1, 2015
    e.g. If it's June 2, 2016, it will start from June 1, 2015
    """
    #if not request.GET.get('iframe', None):
    #    return HttpResponseRedirect('http://dataverse.org')

    one_year_ago = datetime.now() - timedelta(weeks=52)

    # start from the 1st day of last year's month
    date_filters = dict(start_date=one_year_ago.strftime('%Y-%m-01'))

    return view_public_visualizations(request, **date_filters)


#@cache_page(TWO_HOURS_IN_SECONDS)
def view_public_visualizations(request, **kwargs):
    """
    Return HTML/D3Plus visualizations for a variety of public statistics
    """

    if kwargs and len(kwargs) > 0:
        # kwargs override GET parameters
        stats_datasets = StatsMakerDatasets(**kwargs)
        stats_dvs = StatsMakerDataverses(**kwargs)
        stats_files = StatsMakerFiles(**kwargs)
    else:
        stats_datasets = StatsMakerDatasets(**request.GET.dict())
        stats_dvs = StatsMakerDataverses(**request.GET.dict())
        stats_files = StatsMakerFiles(**request.GET.dict())

    # Start an OrderedDict
    resp_dict = OrderedDict()

    # -------------------------
    # Dataverses created each month
    # -------------------------
    stats_result_dv_counts = stats_dvs.get_dataverse_counts_by_month_published()
    #import ipdb; ipdb.set_trace()
    if not stats_result_dv_counts.has_error():
        resp_dict['dataverse_counts_by_month'] = list(stats_result_dv_counts.result_data)
        resp_dict['dataverse_counts_by_month_sql'] = stats_result_dv_counts.sql_query

    # -------------------------
    # Dataverse counts by type
    # -------------------------
    stats_result_dv_counts_by_type =\
        stats_dvs.get_dataverse_counts_by_type_published(exclude_uncategorized=True)
    if not stats_result_dv_counts_by_type.has_error():
        resp_dict['dataverse_counts_by_type'] = stats_result_dv_counts_by_type.result_data
        resp_dict['dv_counts_by_category_sql'] = stats_result_dv_counts_by_type.sql_query


    # -------------------------
    # Datasets created each month
    # -------------------------
    stats_monthly_ds_counts = stats_datasets.get_dataset_counts_by_create_date_published()
    if not stats_monthly_ds_counts.has_error():
        resp_dict['dataset_counts_by_month'] = list(stats_monthly_ds_counts.result_data)
        resp_dict['dataset_counts_by_month_sql'] = stats_monthly_ds_counts.sql_query


    stats_ds_count_by_subject = stats_datasets.get_dataset_subject_counts_published()
    if not stats_monthly_ds_counts.has_error():
        resp_dict['dataset_counts_by_subject'] = stats_ds_count_by_subject.result_data['ds_values']
        #resp_dict['dataset_counts_by_month_sql'] = stats_monthly_ds_counts.sql_query

    # -------------------------
    # Files created, by month
    # -------------------------
    stats_monthly_file_counts = stats_files.get_file_count_by_month_published()
    if not stats_monthly_file_counts.has_error():
        resp_dict['file_counts_by_month'] = list(stats_monthly_file_counts.result_data)
        resp_dict['file_counts_by_month_sql'] = stats_monthly_file_counts.sql_query

    # -------------------------
    # Files downloaded, by month
    # -------------------------
    stats_monthly_downloads = stats_files.get_file_downloads_by_month_published()
    if not stats_monthly_downloads.has_error():
        resp_dict['file_downloads_by_month'] = list(stats_monthly_downloads.result_data)
        resp_dict['file_downloads_by_month_sql'] = stats_monthly_downloads.sql_query

    # -------------------------
    # File counts by content type
    # -------------------------
    # rp: removing this from current charts
    """
    stats_file_content_types = stats_files.get_datafile_content_type_counts_published()
    if not stats_file_content_types.has_error():
        resp_dict['file_content_types'] = list(stats_file_content_types.result_data)
        resp_dict['file_content_types_sql'] = stats_file_content_types.sql_query
        resp_dict['file_content_types_top_20'] = list(stats_file_content_types.result_data)[:20]
        #resp_dict['file_content_types_json'] = json.dumps(file_content_types, indent=4)
    """
    #success, datafile_content_type_counts =\ #stats_files.get_datafile_content_type_counts_published()
    #if success:
    #    resp_dict['datafile_content_type_counts'] = datafile_content_type_counts[:15]



    return render(request, 'metrics/metrics_public.html', resp_dict)



def view_file_extensions_within_type(request, file_type='application/octet-stream'):
    """Query as experiment.  View extensions for unidentified queries"""

    #file_type = 'data/various-formats'
    ids = Datafile.objects.filter(contenttype=file_type).values_list('dvobject__id', flat=True)

    #ids = Datafile.objects.all().values_list('dvobject__id', flat=True)
    l = FileMetadata.objects.filter(datafile__in=ids).values_list('label', flat=True)

    ext_list = [splitext(label)[-1] for label in l]

    extension_counts = {}
    for ext in ext_list:
        extension_counts[ext] = extension_counts.get(ext, 0) + 1

    ext_pairs = extension_counts.items()
    ext_pairs = sorted(ext_pairs, key=lambda k: k[1], reverse=True)

    d = dict(extension_counts=ext_pairs)

    return JsonResponse(d)


def view_files_by_type(request):

    stats_files = StatsMakerFiles(**request.GET.dict())

    # Start an OrderedDict
    resp_dict = OrderedDict()

    # -------------------------
    # Dataverses created each month
    # -------------------------
    success, file_content_types = stats_files.get_datafile_content_type_counts_published()
    if success:
        resp_dict['file_content_types'] = list(file_content_types)
        resp_dict['file_content_types_json'] = json.dumps(file_content_types, indent=4)

    return render(request, 'metrics/visualizations/file_content_types.html', resp_dict)
