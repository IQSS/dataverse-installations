"""
Metric views, returning JSON repsonses
"""

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from dv_apps.utils.date_helper import format_yyyy_mm_dd
from django.db import models
from django.db.models import Count
from dv_apps.datasets.models import Dataset
from dv_apps.dataverses.models import Dataverse
from .stats_util_datasets import StatsMakerDatasets

def view_simple_dataset_count(request):
    """Stripped down example"""

    dataset_count = Dataset.objects.all().count()

    resp_dict = {'dataset_count' : dataset_count}

    return JsonResponse(resp_dict)

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

    dataverse_counts_by_month = Dataverse.objects.filter(id__createdate__year=2015\
        ).annotate(month=TruncMonth('id__createdate')\
        ).values('month'\
        ).annotate(cnt=models.Count('id_id')\
        ).values('month', 'cnt'\
        ).order_by('month')

    dataverse_running_total = 0
    for d in dataverse_counts_by_month:
        dataverse_running_total += d['cnt']
        d['running_total'] = dataverse_running_total
        print d

    dataverse_counts_by_type = Dataverse.objects.values('dataversetype').annotate(type_count=models.Count('dataversetype'))

    d = dict(
        dataset_counts_by_month = dataset_counts_by_month,
        dataverse_counts_by_month = dataverse_counts_by_month,
        dataverse_counts_by_type = dataverse_counts_by_type,
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

class TruncMonth(models.Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()


def view_dataset_counts_by_month(self, selected_year=2016):
    """Counts of datasets by month"""

    dataset_counts_by_month = Dataset.objects.filter(dvobject__createdate__year=selected_year\
        ).annotate(month=TruncMonth('dvobject__createdate')\
        ).values('month'\
        ).annotate(cnt=models.Count('dvobject_id')\
        ).values('month', 'cnt'\
        ).order_by('month')

    year_total_cnt = [x['cnt'] for x in dataset_counts_by_month]


    data_dict = dict(dataset_counts_by_month=list(dataset_counts_by_month),\
                year_count=sum(year_total_cnt))

    ok_dict = dict(status="OK",
                data=data_dict)

    return JsonResponse(ok_dict)


#def view_dataset_counts_by_month2(self):

#    return render('counts_by_month.html', {})
