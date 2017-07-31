import requests
import os
import json
from os.path import isfile
from collections import OrderedDict

from django.shortcuts import render
from dv_apps.utils.message_helper_json import MessageHelperJSON
from django.http import JsonResponse, HttpResponse, Http404
from dv_apps.datafiles.tabular_previewer import TabularPreviewer
from dv_apps.datafiles.models import Datafile
from dv_apps.datafiles.util import DatafileUtil
from dv_apps.datafiles import temp_file_helper

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

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

    file_access_url = DatafileUtil.get_file_access_url(datafile_id)

    temp_filepath, file_ext = temp_file_helper.download_file(file_access_url)

    if temp_filepath is None:
        err_msg = "Failed to download file"
        return False, err_msg, 400

    previewer = TabularPreviewer(temp_filepath, **dict(file_ext=file_ext))

    if previewer.has_error():
        return False, previewer.error_message, 400

    data_rows = previewer.get_data_rows()
    if data_rows is None:
        return False, previewer.error_message, 500
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

    preview_info = data_rows_or_err

    html_summary = preview_info['describe_as_html']
    if html_summary:
        html_summary = html_summary.replace(\
                    'class="dataframe"',
                    'class="summary table table-bordered table-striped"')

    describe_as_dict = preview_info['describe_as_dict']
    if describe_as_dict:
        print type(describe_as_dict)
        json_string = json.dumps(describe_as_dict, indent=4)
        print (json_string)
        formatter = HtmlFormatter(linenos=False, cssclass="friendly")
        json_lexer = get_lexer_by_name("json", stripall=True)
        describe_as_json_snippet = highlight(json_string, json_lexer, formatter)


    info_dict = dict(\
                    column_names=preview_info['column_names'],
                    rows=preview_info['rows'],
                    total_row_count=preview_info['total_row_count'],
                    preview_row_count=preview_info['preview_row_count'],
                    describe_as_json_snippet=describe_as_json_snippet,
                    describe_as_html=html_summary)

    return render(request, 'datafiles/preview_table.html', info_dict)
