"""
Create metrics for Datasets.
This may be used for APIs, views with visualizations, etc.
"""

from django.shortcuts import render
from django.http import JsonResponse
#from django.db.models.functions import TruncMonth  # 1.10
from django.db.models import Count
from django.db import models
from dv_apps.utils.date_helper import format_yyyy_mm_dd
from dv_apps.datasets.models import Dataset

class TruncMonth(models.Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()


class StatsMakerDatasets(object):

    def __init__(self, **kwargs):
        """
        Start and end dates are optional.

        start_date = string in YYYY-MM-DD format
        end_date = string in YYYY-MM-DD format
        """
        self.error_found = False
        self.error_message = None

        # optional datetime objects holding
        self.start_date = None
        self.end_date = None
        self.selected_year = None
        self.bad_http_status_code = None

        # load dates
        self.load_dates_from_kwargs(**kwargs)

    def add_error(self, err_msg, bad_http_status_code=None):
        self.error_found = True
        self.error_message = err_msg
        if bad_status:
            self.bad_http_status_code = bad_http_status_code

    def was_error_found(self):
        return self.error_found

    def get_error_msg_return(self):
        if not self.was_error_found():
            raise AttributeError("Only call this if error_fund is true")
        return False, self.error_message

    def load_dates_from_kwargs(self, **kwargs):

        # Allow start/end date objects
        start_date_str = kwargs.get('start_date', None)
        if start_date_str is not None:
            convert_worked, self.start_date = format_yyyy_mm_dd(start_date_str)
            if not convert_worked:
                self.add_error('Start date is invalid.  Use YYYY-MM-DD format.', 400)
                return

        end_date_str = kwargs.get('end_date', None)
        if self.start_date and end_date_str:
            convert_worked, self.end_date = format_yyyy_mm_dd(end_date_str)
            if not convert_worked:
                self.add_error('End date is invalid.  Use YYYY-MM-DD format.', 400)
                return

            # Make sure start date isn't after end date
            if self.start_date > self.end_date:
                self.add_error('The start date cannot be after the end date.', 400)
                return

        self.selected_year = kwargs.get('selected_year', None)
        if self.selected_year:
            if not (self.selected_year.isdigit() and self.selected_year >= 1000\
                and self.selected_year < 10000):
                self.add_error('The year must be a 4-digit number (YYYY)')
                return




    def get_date_filter_params(self, date_var_name='dvobject__createdate'):
        """
        Create filter params for django queryset

        Default is checking the Dataset create date parameter
        """
        filter_params = {}
        if self.start_date:
            filter_params['%s__gte' % date_var_name] = self.start_date

        if self.end_date:
            filter_params['%s__lte' % date_var_name] = self.end_date

        return filter_params

    def get_dataset_count(self):
        """
        Return the dataset count
        """
        if self.was_error_found():
            return self.get_error_msg_return()

        filter_params = self.get_date_filter_params()

        return True, Dataset.objects.filter(**filter_params).count()

    def get_dataset_count_by_month(self):
        """
        Return dataset counts by month
        """
        if self.was_error_found():
            return self.get_error_msg_return()

        filter_params = self.get_date_filter_params()

        # add date filter
        ds_counts_by_month = Dataset.objects.filter(**filter_params)
        # add the rest of the filters
        ds_counts_by_month = ds_counts_by_month.annotate(\
            month=TruncMonth('dvobject__createdate')\
            ).values('month'\
            ).annotate(cnt=models.Count('dvobject_id')\
            ).values('month', 'cnt'\
            ).order_by('month')

        running_total = 0
        for d in ds_counts_by_month:
            running_total += d['cnt']
            d['running_total'] = running_total
            print d

        return True, ds_counts_by_month
