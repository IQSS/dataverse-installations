import json
from collections import OrderedDict

from django.conf import settings
from django.http import JsonResponse, HttpResponse

from django.views.generic import View
from .stats_util_datasets import StatsMakerDatasets


def send_cors_response(response):
    """Quick hack to allow CORS...."""

    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"

    return response

class DatasetCountByMonth(View):

    """View to Dataset counts by Month"""
    def get(self, request):
        stats_datasets = StatsMakerDatasets(**request.GET.dict())

        stats_result = stats_datasets.get_dataset_counts_by_create_date_published()
        if stats_result.has_error():
            err_dict = dict(status="ERROR",
                message=stats_result.error_message)
            return send_cors_response(JsonResponse(err_dict, status=400))

        resp_dict = OrderedDict()
        resp_dict['status'] = "OK"
        if settings.DEBUG and stats_result.sql_query:
            resp_dict['debug'] = dict(sql_query=stats_result.sql_query)
        resp_dict['data'] = stats_result.result_data


        if 'pretty' in request.GET:
            return HttpResponse('<pre>%s</pre>' % json.dumps(resp_dict, indent=4))

        return send_cors_response(JsonResponse(resp_dict))
