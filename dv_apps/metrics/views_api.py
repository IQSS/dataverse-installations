"""
Metric views, returning JSON repsonses
"""
import json
from collections import OrderedDict

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db import models
from django.db.models import Count

from dv_apps.utils.date_helper import format_yyyy_mm_dd
from dv_apps.datasets.models import Dataset
from dv_apps.dataverses.models import Dataverse
from dv_apps.guestbook.models import GuestBookResponse
from .stats_util_datasets import StatsMakerDatasets


def view_dataset_counts_by_month(request):

    stats_datasets = StatsMakerDatasets(**request.GET.dict())

    stats_result = stats_datasets.get_dataset_counts_by_create_date_published()
    if stats_result.has_error():
        err_dict = dict(status="ERROR",
            message=stats_result.error_message)
        return JsonResponse(err_dict, status=400)

    resp_dict = OrderedDict()
    resp_dict['status'] = "OK"
    if settings.DEBUG and stats_result.sql_query:
        resp_dict['debug'] = dict(sql_query=stats_result.sql_query)
    resp_dict['data'] = stats_result.result_data


    if 'pretty' in request.GET:
        return HttpResponse('<pre>%s</pre>' % json.dumps(resp_dict, indent=4))

    response = JsonResponse(resp_dict)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response




def view_simple_dataset_count(request):
    """Stripped down example"""

    dataset_count = Dataset.objects.all().count()

    resp_dict = {'dataset_count' : dataset_count}

    return JsonResponse(resp_dict)


class TruncMonth(models.Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()


def view_jcabanas(request):

    dataset_counts_by_month = Dataset.objects.filter(dvobject__createdate__year=2015\
        ).annotate(month=TruncMonth('dvobject__createdate')\
        ).values('month'\
        ).annotate(cnt=models.Count('dvobject_id')\
        ).values('month', 'cnt'\
        ).order_by('month')

    running_total = 0
    for d in dataset_counts_by_month:
        running_total += d['cnt']
        d['running_total'] = running_total
        print d

    smd = StatsMakerDatasets()

    success, count_test = smd.get_dataset_count()
    if not success:
        return JsonResponse(smd.get_http_error_dict(), status=smd.get_http_err_code())

    print count_test

    dataverse_counts_by_month = Dataverse.objects.filter(dvobject__createdate__year=2015\
        ).annotate(month=TruncMonth('dvobject__createdate')\
        ).values('month'\
        ).annotate(cnt=models.Count('dvobject_id')\
        ).values('month', 'cnt'\
        ).order_by('month')

    dataverse_running_total = 0
    for d in dataverse_counts_by_month:
        dataverse_running_total += d['cnt']
        d['running_total'] = dataverse_running_total
        print d

    dataverse_counts_by_type = Dataverse.objects.values('dataversetype').annotate(type_count=models.Count('dataversetype'))

    file_counts_by_month = GuestBookResponse.objects.filter(downloadtype='Download'\
        ).annotate(month=TruncMonth('responsetime')\
        ).values('month'\
        ).annotate(cnt=models.Count('guestbook_id')\
        ).values('month', 'cnt'\
        ).order_by('month')

    file_running_total = 0
    for d in file_counts_by_month:
        file_running_total += d['cnt']
        d['running_total'] = file_running_total
        print d


    d = dict(
        dataset_counts_by_month = dataset_counts_by_month,
        dataverse_counts_by_month = dataverse_counts_by_month,
        dataverse_counts_by_type = dataverse_counts_by_type,
        file_counts_by_month = file_counts_by_month,
    )



    return render(request, 'metrics.html', d)


def view_dataset_count(request):
    """Return the dataset count
    Optional params:
        start_date = YYYY-MM-DD
        end_date = YYYY-MM-DD
    start_date may be used without end date
    """
    #import ipdb; ipdb.set_trace()

    filter_params = {}
    resp_dict = {}

    start_date_str = request.GET.get('start_date', None)
    end_date_str = request.GET.get('end_date', None)

    """Format the start date and add it to the query"""
    if start_date_str is not None:
        convert_worked, sdate = format_yyyy_mm_dd(start_date_str)
        if not convert_worked:
            err_dict = dict(status="ERROR",
                        message='Start date is invalid.  Use YYYY-MM-DD format.')
            return JsonResponse(err_dict, status=400)

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

    dataset_count = Dataset.objects.filter(**filter_params).count()

    resp_dict['dataset_count'] = dataset_count
    ok_dict = dict(status="OK",
                data=resp_dict)
    return JsonResponse(ok_dict)
