"""
Metric views, returning JSON repsonses
"""
from collections import OrderedDict
import json
from random import randint

from os.path import splitext

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import cache_page
from django.http import JsonResponse, HttpResponse
from django.db import models
from django.db.models import Count
from django.db.models import F

from dv_apps.utils.date_helper import format_yyyy_mm_dd
from dv_apps.datafiles.models import Datafile, FileMetadata
from dv_apps.datasets.models import Dataset
from dv_apps.dvobjects.models import DvObject, DTYPE_DATAVERSE
from dv_apps.dataverses.models import Dataverse
from dv_apps.guestbook.models import GuestBookResponse
from dv_apps.metrics.stats_util_datasets import StatsMakerDatasets
from dv_apps.metrics.stats_util_dataverses import StatsMakerDataverses
from dv_apps.metrics.stats_util_files import StatsMakerFiles


def view_dataverse_tree(request):

    d = {}

    return render(request, 'viz-tree/bostock_tree.html', d)

def view_dataverse_tree2(request):

    d = {}

    return render(request, 'viz-tree/rob-tree.html', d)


def get_dataverse_tree_json(request):

    # Note: "F(..) allows aliasing of a field.  e.g. SELECT dvobject as id,...
    dvs = Dataverse.objects.select_related('dvobject').annotate(id=F('dvobject'), parent_id=F('dvobject__owner__id')).values('id', 'parent_id', 'name').all().order_by('name')

    parent_child_lists = {} #{ parent_id : [ info, info, info ]}
    root_node = None
    for dv_info in dvs:
        if dv_info['parent_id'] is None:
            root_node = dv_info
        else:
            parent_child_lists.setdefault(dv_info['parent_id'], []).append(dv_info)

    print parent_child_lists
    print 'root_node', root_node

    full_tree = get_child_nodes(root_node, parent_child_lists)
    print '-' * 40
    print json.dumps(full_tree, indent=4)
    print '-' * 40

    fmt_list = []
    for info in full_tree.get('children'):
        if info.has_key('children'):
            fmt_list.append(info)

    full_tree['children'] = fmt_list
    
    return JsonResponse(full_tree)

def get_child_nodes(root_node, parent_child_lists, depth=0):

    child_nodes = parent_child_lists.get(root_node['id'], None)

    # Are there child nodes?
    if not child_nodes:
        return OrderedDict(name=root_node['name'], value=randint(400, 500), depth=depth)
    else:
        child_list = [] # create child list
        for cn in child_nodes:
            child_tree = get_child_nodes(cn, parent_child_lists, depth=depth+1)
            if child_tree and len(child_tree) > 0:
                child_list.append(child_tree)

        fmt_d = OrderedDict()
        fmt_d['name'] = root_node['name']
        fmt_d['children'] = child_list
        fmt_d['depth'] = depth
        return fmt_d
