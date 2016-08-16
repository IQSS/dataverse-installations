from django.views.decorators.cache import cache_page
from django.shortcuts import render
from django.template.loader import render_to_string

from django.http import HttpResponse
from django.conf import settings

from dv_apps.metrics.stats_views_datasets import DatasetCountByMonthView
from dv_apps.metrics.stats_views_dataverses import DataverseTotalCounts,\
    DataverseCountByMonthView,\
    DataverseAffiliationCounts,\
    DataverseTypeCounts
from dv_apps.metrics.stats_views_files import FileCountByMonthView,\
    FileTotalCountsView,\
    FilesDownloadedByMonthView,\
    FileCountsByContentTypeView,\
    FileExtensionsWithinContentType


"""
Make a list of class based views
    (each one has a "get_swagger_spec()" method)
"""
VIEW_CLASSES_FOR_SPEC = [DataverseTotalCounts,\
            DataverseCountByMonthView,\
            DataverseAffiliationCounts,\
            DataverseTypeCounts,\
            DatasetCountByMonthView,\
            FileTotalCountsView,\
            FileCountByMonthView,\
            FilesDownloadedByMonthView,\
            FileCountsByContentTypeView,\
            FileExtensionsWithinContentType
            ]

#@cache_page(60*3)
def view_dynamic_swagger_spec(request):
    global VIEW_CLASSES_FOR_SPEC

    # Iterate through the class-based views and
    # generate a swagger spec for each endpoint
    endpoints = []
    for vclass in VIEW_CLASSES_FOR_SPEC:
        endpoints.append(vclass().get_swagger_spec())

    # Add the endpoints to a dict
    d = dict(endpoints=endpoints,\
             SWAGGER_HOST=settings.SWAGGER_HOST,\
             SWAGGER_SCHEME=settings.SWAGGER_SCHEME)

    # render the full swagger spec
    yaml_spec = render_to_string('swagger_spec/basic_spec_01.yaml', d)

    return HttpResponse(yaml_spec)



def view_swagger_spec_test(request):
    """Show the swaggger spec!"""
    spec = """swagger: "2.0"

info:
  version: 0.5.0
  title: Dataverser Metrics API
  description: An API for Dataverse metrics. (internal use)

schemes:
  - http
host: 127.0.0.1:8000
basePath: /metrics/v1

paths:
  /datasets/count/monthly:
    get:
      summary: Number of new Datasets added each month
      description: Returns a list of counts and cumulative counts of all datasts added in a month
      parameters:
        - $ref: "#/parameters/startDateParam"
        - $ref: "#/parameters/endDateParam"
        - $ref: "#/parameters/selectedYearParam"
        - $ref: "#/parameters/prettyJSONParam"
      responses:
        200:
          description: A list of Dataset counts by month
          schema:
            $ref: "#/definitions/MonthCounts"
        400:
          description: Parameter error


# define reusable parameters:
parameters:
  startDateParam:
    name: start_date
    in: query
    description: Optional. Inclusive start date in YYYY-MM-DD format
    type: string
  endDateParam:
    name: end_date
    in: query
    description: Optional. Inclusive end date in YYYY-MM-DD format
    type: string
  selectedYearParam:
    name: selected_year
    in: query
    description: Optional. Selected year in YYYY format
    type: string
  timeSortParam:
    name: time_sort
    in: query
    description: Optional. Sort by time.  'a' = ascending; 'd' = descending
    type: string
  prettyJSONParam:
    name: pretty
    in: query
    description: Optional. Returns HTML response showing formatted JSON
    type: boolean

definitions:
  MonthCount:
    properties:
      cnt:
        type: integer
      running_total:
        type: integer
      yyyy_mm:
        type: string
      month_name:
        type: string
      year_num:
        type: integer
      month_num:
        type: integer
  MonthCounts:
    type: array
    items:
      $ref: "#/definitions/MonthCount"
"""

    response = HttpResponse(spec)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

    #return HttpResponse(spec)
