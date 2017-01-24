import requests
import os
from os.path import isfile
from django.shortcuts import render
from dv_apps.utils.message_helper_json import MessageHelperJSON
from django.http import JsonResponse, HttpResponse, Http404
from dv_apps.datafiles.tabular_previewer import TabularPreviewer
from dv_apps.datafiles.models import Datafile
from dv_apps.datafiles import temp_file_helper

from django.conf import settings

from dv_apps.utils import query_helper
from django.views.decorators.cache import cache_page


def get_table_rows(datafile_id):

    if not datafile_id:
        err_msg = "No file id specified"
        return False, err_msg, 400

    is_published_param = query_helper.get_is_published_filter_param()

    datafile = Datafile.objects.select_related('dvobject'
                        ).filter(**is_published_param
                        ).filter(dvobject__id=datafile_id).first()

    if datafile is None:
        err_msg = "No published file found with id: %s" % datafile_id
        return False, err_msg, 404

    file_access_url = 'https://dataverse.harvard.edu/api/access/datafile/%s' % datafile_id

    temp_filepath = temp_file_helper.download_file(file_access_url)

    if temp_filepath is None:
        err_msg = "Failed to download file"
        return False, err_msg, 400

    previewer = TabularPreviewer(temp_filepath)

    if previewer.has_error():
        return False, previewer.error_message, 400


    data_rows = previewer.get_data_rows()

    # We have the rows, delete the downloaded file
    # In future, cache or save preview rows to db, etc.
    #
    temp_file_helper.make_sure_file_deleted(temp_filepath)

    return True, data_rows, 200



#@cache_page(600)
@cache_page(settings.METRICS_CACHE_VIEW_TIME)
def view_table_preview_json(request, datafile_id):
    """Return first rows of a tabular file for AJAX use"""

    success, data_rows_or_err, http_status_code = get_table_rows(datafile_id)

    if not success:
        json_msg = MessageHelperJSON.get_json_fail_msg(data_rows_or_err)
        return HttpResponse(status=http_status_code,
                            content=json_msg,
                            content_type="application/json")

    json_success_msg = MessageHelperJSON.get_json_success_msg(data_dict=data_rows_or_err)

    return HttpResponse(content=json_success_msg,
                        content_type="application/json")



@cache_page(settings.METRICS_CACHE_VIEW_TIME)
def view_table_preview_html(request, datafile_id):

    success, data_rows_or_err, http_status_code = get_table_rows(datafile_id)

    if not success:
        return HttpResponse(status=http_status_code,
                        content=data_rows_or_err)


    info_dict = dict(column_names=data_rows_or_err['column_names'],
                    rows=data_rows_or_err['rows'],
                    total_row_count=data_rows_or_err['total_row_count'],
                    preview_row_count=data_rows_or_err['preview_row_count']
                    )

    return render(request, 'datafiles/preview_table.html', info_dict)
