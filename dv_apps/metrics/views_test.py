"""
Metric views, returning JSON repsonses
"""
from collections import OrderedDict
import json
from os.path import splitext

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import cache_page
from django.http import JsonResponse, HttpResponse
from django.db import models
from django.db.models import Count

from dv_apps.utils.date_helper import format_yyyy_mm_dd
from dv_apps.datafiles.models import Datafile, FileMetadata
from dv_apps.datasets.models import Dataset
from dv_apps.dataverses.models import Dataverse
from dv_apps.guestbook.models import GuestBookResponse
from dv_apps.metrics.stats_util_datasets import StatsMakerDatasets
from dv_apps.metrics.stats_util_dataverses import StatsMakerDataverses
from dv_apps.metrics.stats_util_files import StatsMakerFiles


def view_dataverse_tree(request):

    d = {}
    return render(request, 'visualizations/bostock_tree.html', d)
