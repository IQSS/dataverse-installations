"""
Metric views, returning JSON repsonses
"""
from collections import OrderedDict

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from dv_apps.utils.date_helper import format_yyyy_mm_dd
from django.db import models
from django.db.models import Count
from dv_apps.datasets.models import Dataset
from dv_apps.dataverses.models import Dataverse
from dv_apps.guestbook.models import GuestBookResponse
from .stats_util_datasets import StatsMakerDatasets


def view_public_visualizations(request):

    smd = StatsMakerDatasets(**request.GET.dict())

    # Start an OrderedDict
    resp_dict = OrderedDict()

    # -------------------------
    # Dataverses created each month
    # -------------------------
    success, dataverse_counts_by_month = smd.get_dataverse_counts_by_month()
    if success:
        resp_dict['dataverse_counts_by_month'] = list(dataverse_counts_by_month)

    # -------------------------
    # Datasets created each month
    # -------------------------
    success, dataset_counts_by_month = smd.get_dataset_counts_by_create_date()
    if success:
        resp_dict['dataset_counts_by_month'] = list(dataset_counts_by_month)

    # -------------------------
    # Dataverse counts by type
    # -------------------------
    success, dataverse_counts_by_type = smd.get_dataverse_counts_by_type()
    if success:
        resp_dict['dataverse_counts_by_type'] = dataverse_counts_by_type

    # -------------------------
    # File counts by month
    # -------------------------
    success, file_counts_by_month = smd.get_downloads_by_month()
    if success:
        resp_dict['file_counts_by_month'] = list(file_counts_by_month)


    return render(request, 'metrics_public.html', resp_dict)
