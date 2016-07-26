"""
Metric views, returning JSON repsonses
"""

from django.shortcuts import render
from collections import OrderedDict
import json
from django.http import JsonResponse, HttpResponse
from dv_apps.utils.date_helper import format_yyyy_mm_dd
from django.db import models
from .stats_util_datasets import StatsMakerDatasets
from dv_apps.datasets.models import Dataset

def view_simple_dataset_count2(request):
    """Stripped down example"""

    smd = StatsMakerDatasets(**request.GET.dict())


    success, dataset_count = smd.get_dataset_count()
    
    if not success:
        return JsonResponse(smd.get_http_error_dict(), status=smd.get_http_err_code())

    resp_dict = OrderedDict({'dataset_count' : dataset_count})

#<<<<<<< Updated upstream
    success, dataset_counts_by_month = smd.get_dataset_counts_by_create_date()
#=======
    success, dataset_counts_by_month = smd.get_dataset_count_by_month()
    
#>>>>>>> Stashed changes
    if success:
        resp_dict['dataset_counts_by_month'] = list(dataset_counts_by_month)

    success, datasets_published_counts_by_month = smd.get_dataset_counts_by_publication_date()
    if success:
        resp_dict['datasets_published_counts_by_month'] = list(datasets_published_counts_by_month)


    return HttpResponse('<pre>' + json.dumps(resp_dict, indent=4) + '</pre>')
    return JsonResponse(resp_dict)
