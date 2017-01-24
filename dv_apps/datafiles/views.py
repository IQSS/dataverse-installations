from django.shortcuts import render
from django.http import HttpResponse, Http404

from dv_apps.datafiles.tabular_previewer import TabularPreviewer
from dv_apps.datafiles.models import Datafile

from dv_apps.utils import query_helper

def view_table_preview_json(request, datafile_id):
    """Return tabular file rows as JSON"""

    is_published_param = query_helper.get_is_published_filter_param()

    datafile = Datafile.objects.select_related('dvobject'\
                        ).filter(**is_published_param\
                        ).filter(dvobject__id=datafile_id).first()

    if datafile is None:
        raise Http404("no file found")
