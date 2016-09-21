"""
Metric views, returning JSON repsonses
"""
from collections import OrderedDict
import json


from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db.models import F

from dv_apps.dataverses.models import Dataverse
from dv_apps.metrics.dataverse_tree_util import DataverseTreeUtil
from dv_apps.metrics.stats_datasets_bins import FilesPerDatasetCounter



def view_metrics_links(request):
    d = {}
    return render(request, 'metrics/view_metrics_links.html', d)


def view_dataverse_tree(request):

    d = {}

    return render(request, 'metrics/viz-tree/bostock_tree.html', d)

def view_dataverse_tree2(request):

    d = {}

    return render(request, 'metrics/viz-tree/rob-tree.html', d)

def get_dataverse_full_tree_json(request):
    """Return JSON with the full Datavese "tree" -- e.g. parent/child relations"""

    return get_dataverse_tree_json(request, skip_flat_dataverses=False)


def get_dataverse_tree_json(request, skip_flat_dataverses=True):

    dtu = DataverseTreeUtil()

    tree_dict = dtu.get_dataverse_tree_dict(skip_flat_dataverses=skip_flat_dataverses)

    if 'pretty' in request.GET:
        as_html = '<pre>%s</pre>' % (json.dumps(tree_dict, indent=4))
        return HttpResponse(as_html)

    return JsonResponse(tree_dict)

def view_file_bins_by_datasetversion(request):

    fdc = FilesPerDatasetCounter()
    print fdc.get_counts()
    d = dict(bin_info=fdc.get_counts())

    return render(request, 'metrics/visualizations/file_bins_by_datasetversion.html', d)
