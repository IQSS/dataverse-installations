"""
Metric views, returning JSON repsonses
"""
from collections import OrderedDict
import json


from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db.models import F

from dv_apps.dataverses.models import Dataverse
from dv_apps.metrics.dataverse_tree_util import get_dataverse_tree_dict



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

    tree_dict = get_dataverse_tree_dict(skip_flat_dataverses=skip_flat_dataverses)

    as_html = '<pre>%s</pre>' % (json.dumps(tree_dict, indent=4))

    return HttpResponse(as_html)

    return JsonResponse(tree_dict)
