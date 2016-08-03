"""
Metric views, returning JSON repsonses
"""
from collections import OrderedDict
import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import cache_page

from dv_apps.utils.date_helper import format_yyyy_mm_dd
from django.db import models
from django.db.models import Count
from dv_apps.datasets.models import Dataset
from dv_apps.dataverses.models import Dataverse
from dv_apps.guestbook.models import GuestBookResponse
from .stats_util_datasets import StatsMakerDatasets
from .stats_util_dataverses import StatsMakerDataverses
from .stats_util_files import StatsMakerFiles

#@cache_page(60 * 15)
def view_public_visualizations(request):

    stats_datasets = StatsMakerDatasets(**request.GET.dict())
    stats_dvs = StatsMakerDataverses(**request.GET.dict())
    stats_files = StatsMakerFiles(**request.GET.dict())

    # Start an OrderedDict
    resp_dict = OrderedDict()

    # -------------------------
    # Dataverses created each month
    # -------------------------
    success, dataverse_counts_by_month = stats_dvs.get_dataverse_counts_by_month()
    if success:
        resp_dict['dataverse_counts_by_month'] = list(dataverse_counts_by_month)

    # -------------------------
    # Datasets created each month
    # -------------------------
    success, dataset_counts_by_month = stats_datasets.get_dataset_counts_by_create_date_published()
    if success:
        resp_dict['dataset_counts_by_month'] = list(dataset_counts_by_month)

    # -------------------------
    # Dataverse counts by type
    # -------------------------
    success, dataverse_counts_by_type =\
        stats_dvs.get_dataverse_counts_by_type_published(exclude_uncategorized=True)
    if success:
        resp_dict['dataverse_counts_by_type'] = dataverse_counts_by_type


    #success, datafile_content_type_counts = stats_files.get_datafile_content_type_counts_published()
    success, datafile_content_type_counts = stats_files.get_datafile_content_type_counts()
    if success:
        resp_dict['datafile_content_type_counts'] = datafile_content_type_counts[:15]
        #resp_dict['JSON_STATS'] = json.dumps(datafile_content_type_counts)

    success, file_downloads_by_month = stats_files.get_file_downloads_by_month_published()
    if success:
        resp_dict['file_downloads_by_month'] = list(file_downloads_by_month)
        print 'file_downloads_by_month', file_downloads_by_month
    """

    # -------------------------
    # File counts by month
    # -------------------------
    success, file_counts_by_month = smd.get_downloads_by_month()
    if success:
        resp_dict['file_counts_by_month'] = list(file_counts_by_month)
    """

    return render(request, 'visualizations/metrics_public.html', resp_dict)
