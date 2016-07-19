from django.shortcuts import render
from django.http import JsonResponse
from dv_apps.datasets.models import Dataset

def view_dataset_count(request):    #, start_date=None, end_date=None):
    """Return the dataset count"""
    dataset_count = Dataset.objects.all().count()

    d = dict(dataset_count=dataset_count)

    return JsonResponse(d)
