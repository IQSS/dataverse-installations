from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import cache_page
from django.http import JsonResponse, HttpResponse
from django.db import models
from django.db.models import Count
from django.db.models import F

def view_swagger_spec(request):
    """Show the swaggger spec!"""
    spec = """swagger: "2.0"

info:
  version: 1.0.0
  title: Metrics API
  description: A simple API to learn how to write OpenAPI Specification

schemes:
  - http
host: 127.0.0.1:8000
basePath: /metrics/v1

paths:
  /datasets/count/monthly:
    get:
      summary: Number of new Datasets added each month
      description: Returns a list of counts and cumulative counts of all datasts added in a month
      responses:
        200:
          description: A list of Dataset counts by month
          schema:
            type: array
            items:
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
"""

    response = HttpResponse(spec)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

    #return HttpResponse(spec)
