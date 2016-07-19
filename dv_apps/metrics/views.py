from django.shortcuts import render
from django.http import JsonResponse

def view_dataset_count(request):
    """Return the dataset count"""
    #import ipdb; ipdb.set_trace()
    from dv_apps.datasets.models import Dataset

    dataset_count = Dataset.objects.all().count()

    d = dict(dataset_count=dataset_count)

    return JsonResponse(d)
