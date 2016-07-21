"""
Metric views, returning JSON repsonses
"""
from django.shortcuts import render
from django.http import JsonResponse
from dv_apps.utils.date_helper import format_yyyy_mm_dd

from dv_apps.datasets.models import Dataset

def view_simple_dataset_count(request):
    """Stripped down example"""

    dataset_count = Dataset.objects.all().count()

    resp_dict = {'dataset_count' : dataset_count}

    return JsonResponse(resp_dict)


def view_dataset_count(request, start_date_str=None, end_date_str=None):
    """Return the dataset count"""
    #import ipdb; ipdb.set_trace()

    filter_params = {}
    resp_dict = {}

    """Format the start date and add it to the query"""
    if start_date_str is not None:
        convert_worked, sdate = format_yyyy_mm_dd(start_date_str)
        if not convert_worked:
            resp_dict['status'] = 'error'
            resp_dict['results'] = [dict(message="Start date is invalid.  Use YYYY-MM-DD format.", code='InvalidArgument')]
            return JsonResponse(resp_dict, status=400)

        filter_params['dvobject__createdate__gte'] = sdate
        resp_dict['start_date'] = sdate.date()

    """Format the end date and add it to the query"""
    if end_date_str is not None:
        convert_worked, edate = format_yyyy_mm_dd(end_date_str)
        if not convert_worked:
            err_dict = dict(status="ERROR",
                        message='End date is invalid.  Use YYYY-MM-DD format.')
            return JsonResponse(err_dict, status=400)

        if sdate > edate:
            err_dict = dict(status="ERROR",
                        message='The start date cannot be after the end date.')
            return JsonResponse(err_dict, status=400)

        filter_params['dvobject__createdate__lte'] = edate
        resp_dict['end_date'] = edate.date()



    print('filter_params', filter_params)
    dataset_count = Dataset.objects.filter(**filter_params).count()
    #resp_dict['status'] = 'success'

    resp_dict['dataset_count'] = dataset_count
    ok_dict = dict(status="OK",
                data=resp_dict)
    return JsonResponse(ok_dict)
