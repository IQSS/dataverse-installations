"""
Metric views, returning JSON repsonses
"""

from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponse
from dv_apps.utils.date_helper import format_yyyy_mm_dd
from django.db import models
from .stats_util_datasets import StatsMakerDatasets
from dv_apps.datasets.models import Dataset

def view_simple_dataset_count2(request):
    """Stripped down example"""

    kwargs = dict(start_date=request.GET.get('start_date', None),\
                end_date=request.GET.get('end_date', None),\
                selected_year=request.GET.get('selected_year', None))
    smd = StatsMakerDatasets(**kwargs)

    success, dataset_count = smd.get_dataset_count()
    if not success:
        return JsonResponse(smd.get_http_error_dict(), status=smd.get_http_err_code())

    resp_dict = {'dataset_count' : dataset_count}

    success, dataset_counts_by_month = smd.get_dataset_count_by_month()
    if success:
        resp_dict['dataset_counts_by_month'] = list(dataset_counts_by_month)

    return HttpResponse('<pre>' + json.dumps(resp_dict, indent=4) + '</pre>')
    return JsonResponse(resp_dict)
