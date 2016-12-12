import json
import csv
from collections import OrderedDict
from datetime import datetime
from StringIO import StringIO
#import pandas as pd

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string

from django.views.generic import View

# Apply API Key and page caching to API endpoints
#
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from dv_apps.dataverse_auth.decorator import apikey_required
from dv_apps.utils.metrics_cache_time import get_metrics_api_cache_time
from dv_apps.utils.date_helper import get_timestamp_for_filename

from dv_apps.metrics.stats_util_base import StatsMakerBase

def send_cors_response(response):
    """Quick hack to allow CORS...."""

    response["Access-Control-Allow-Origin"] = "*"
    #response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    #response["Access-Control-Max-Age"] = "1000"
    #response["Access-Control-Allow-Headers"] = "*"

    return response

@method_decorator(apikey_required, name='get')
@method_decorator(cache_page(get_metrics_api_cache_time()), name='get')
class StatsViewSwagger(View):
    """Used to help build the swagger docs"""

    # params getting a bit out of control, need to make this more manageable

    BASIC_DATE_PARAMS = ['startDateParam', 'endDateParam', 'selectedYearParam']

    PARAM_DV_API_KEY = ['dataverseAPIKey']
    PARAM_SELECTED_DV_ALIASES = ['selectedDataverseAliases']
    PARAM_INCLUDE_CHILD_DVS = ['includeChildDataverses']
    PARAM_AS_CSV = ['asCSV', 'asExcel']

    PARAM_BIN_SIZE = ['binSize']  # bin_size
    PARAM_NUM_BINS = ['numBins']  # num_bins
    PARAM_SKIP_EMPTY_BINS = ['skipEmptyBins'] # skip_empty_bins
    PARAM_DVOBJECT_ID = ['dataverseObjectId']
    PARAM_DATASET_ID = ['datasetId']
    PARAM_DATASET_PERSISTENT_ID = ['persistentId']

    PARAM_DATAVERSE_ALIAS = ['dataverseAlias']

    PUBLISH_PARAMS = ['publicationStateParam']
    PUB_STATE_PUBLISHED = 'published'
    PUB_STATE_UNPUBLISHED = 'unpublished'
    PUB_STATE_ALL = 'all'

    PRETTY_JSON_PARAM = ['prettyJSONParam']
    DV_TYPE_UNCATEGORIZED_PARAM = ['showUncategorizedParam']
    FILE_CONTENT_TYPE_PARAM = ['contentTypeParam']

    RESULT_NAME_MONTH_COUNTS = 'MonthCounts'
    RESULT_NAME_FILE_EXT_COUNTS = 'FileExtensionCounts'
    RESULT_NAME_FILE_TYPE_COUNTS = 'FileTypeCounts'

    RESULT_NAME_TOTAL_COUNT = 'TotalCount'
    RESULT_NAME_NUM_UNIQUE_EXT = 'NumberUniqueExtensions'
    RESULT_NAME_AFFILIATION_COUNTS = 'AffiliationCounts'
    RESULT_NAME_DATASET = 'Dataset'
    RESULT_NAME_DATAVERSE = 'Dataverse'
    RESULT_NAME_DATAVERSE_TYPE_COUNTS = 'DataverseTypeCount'
    RESULT_NAME_DATASET_SUBJECT_COUNTS = 'DatasetSubjectCounts'
    RESULT_NAME_BIN_COUNTS = 'BinCounts'

    TAG_METRICS = 'metrics'
    TAG_DATAVERSES = 'metrics - dataverses'
    TAG_DATASETS = 'metrics - datasets'
    TAG_DATAFILES = 'metrics - files'
    TAG_TEST_API = 'dataverse/dataset JSON - (test, may go away)'

    # ---------------------------------------------
    # For holding errors found at the SwaggerView level
    #   - e.g. bad url params not caught at a lower level
    # ---------------------------------------------
    error_found = False
    error_message = None

    # ---------------------------------------------
    # Swagger attributes to be defined for each subclass
    # ---------------------------------------------
    api_path = '/path/to/endpoint'
    summary = 'add summary'
    description = 'add description'
    description_200 = 'description for the HTTP 200 response'
    param_names = PARAM_DV_API_KEY + BASIC_DATE_PARAMS + PUBLISH_PARAMS + PRETTY_JSON_PARAM
    result_name = RESULT_NAME_MONTH_COUNTS
    tags = [TAG_METRICS]
    # ---------------------------------------------



    def get_swagger_spec(self):
        """Return a YAML representation of the swagger spec for this endpoint"""

        d = {}
        d['api_path'] = self.api_path
        d['summary'] = self.summary
        d['description'] = self.description
        d['description_200'] = self.description_200
        d['param_names'] = self.param_names
        d['result_name'] = self.result_name
        d['tags'] = self.tags

        return render_to_string('metrics/swagger_spec/single_endpoint.yaml', d)

    def get_content_type_param(self, request):
        """Return the result of the "?unpublished" query string param"""
        ctype = request.GET.get('ctype', None)   # add this as variable..
        if ctype is not None and len(ctype) > 0:
            return ctype
        return None

    def get_pub_state(self, request):
        """Return the result of the "?pub_state" query string param
        Default value is: "published"
        Other choices: "unpublished", "all"
        When checking, use:
            - PUB_STATE_PUBLISHED
            - PUB_STATE_UNPUBLISHED
            - PUB_STATE_ALL
        """
        return request.GET.get('pub_state', self.PUB_STATE_PUBLISHED)


    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic.
        Overwrite this method for each subclass
        """
        raise Exception("This method must return a stats_result.StatsResult object")


    def get(self, request, *args, **kwargs):
        """Return a basic get request using the StatsResult object"""

        # Get the StatsResult -- different for each subclass
        stats_result = self.get_stats_result(request)
        if stats_result is None:
            err_dict = dict(status="ERROR",\
                    message="Unknown processing error")
            return send_cors_response(JsonResponse(err_dict, status=500))

        # Was there an error? If so, return the error message
        #
        if stats_result.has_error():
            err_dict = dict(status="ERROR",
                message=stats_result.error_message)
            if stats_result.bad_http_status_code:
                status_code = stats_result.bad_http_status_code
            else:
                status_code = 400
            return send_cors_response(JsonResponse(err_dict, status=status_code))


        # Create the dict for the response
        #
        resp_dict = OrderedDict()

        # status is "OK"
        resp_dict['status'] = "OK"

        # Is we're in debug and the SQL query is available,
        #   send it in
        if settings.DEBUG and stats_result.sql_query:
            resp_dict['debug'] = dict(sql_query=stats_result.sql_query)

        # Set a timestamp and params
        resp_dict['info'] = OrderedDict()
        resp_dict['info']['generation_time'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        if get_metrics_api_cache_time() > 0:
            resp_dict['info']['cache_time_seconds'] = get_metrics_api_cache_time()
        resp_dict['info']['params'] = request.GET

        # Set the actual stats data
        resp_dict['data'] = stats_result.result_data


        # Is there a request to send the JSON formatted within HTML tags?
        if 'pretty' in request.GET:
            return HttpResponse('<pre>%s</pre>' % json.dumps(resp_dict, indent=4))

        if StatsMakerBase.is_param_value_true(request.GET.get('as_csv', None)):
            return self.get_data_as_csv_response(request, stats_result)

        if StatsMakerBase.is_param_value_true(request.GET.get('as_excel', None)):
            return self.get_data_as_excel_response(request, stats_result)


        # Return the actual response
        return send_cors_response(JsonResponse(resp_dict))


    def get_data_as_csv_response(self, request, stats_result):
        """Hasty method, proof of concept for downloads by month"""
        if stats_result is None or stats_result.result_data is None:
            return None


        csv_content = stats_result.get_csv_content()

        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(csv_content, content_type='text/csv')

        csv_fname = 'metrics_%s.csv' % get_timestamp_for_filename()
        response['Content-Disposition'] = 'attachment; filename="%s"' % csv_fname

        return response


    def get_data_as_excel_response(self, request, stats_result):
        """
        http://stackoverflow.com/questions/35267585/django-pandas-to-http-response-download-file
        """
        if stats_result is None or stats_result.result_data is None:
            return None

        excel_workbook = stats_result.get_excel_workbook()
        if excel_workbook is None:
            # Ah, make a better error
            return HttpResponse('Sorry! An error occurred trying to create an Excel spreadsheet.')


        xlsx_fname = 'metrics_%s.xlsx' % get_timestamp_for_filename()

        response = HttpResponse(excel_workbook,\
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=%s' % xlsx_fname

        return response
