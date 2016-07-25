"""
Create metrics for Datasets.
This may be used for APIs, views with visualizations, etc.
"""

from django.shortcuts import render
from django.http import JsonResponse
#from django.db.models.functions import TruncMonth  # 1.10
from django.db.models import Count
from django.db import models
from dv_apps.utils.date_helper import format_yyyy_mm_dd, get_month_name
from dv_apps.datasets.models import Dataset

class TruncMonth(models.Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()

class TruncYearMonth(models.Func):
    function = 'to_char'
    template = "%(function)s(%(expressions)s, 'YYYY-MM')"
    output_field = models.CharField()

    #to_char(createdate, 'YYYY-MM')

class StatsMakerDatasets(object):

    def __init__(self, **kwargs):
        """
        Start and end dates are optional.

        start_date = string in YYYY-MM-DD format
        end_date = string in YYYY-MM-DD format
        """
        # error related variables
        self.error_found = False
        self.error_message = None
        self.bad_http_status_code = None

        # optional datetime objects holding
        self.start_date = None
        self.end_date = None
        self.selected_year = None
        self.time_sort = None


        # load dates
        self.load_dates_from_kwargs(**kwargs)

    def add_error(self, err_msg, bad_http_status_code=None):
        self.error_found = True
        self.error_message = err_msg
        if bad_http_status_code:
            self.bad_http_status_code = bad_http_status_code

    def was_error_found(self):
        return self.error_found


    def get_http_error_dict(self):
        """
        Return a dict usable in a JsonResponse object
        """
        if not self.was_error_found():
            raise AttributeError("Only call this if was_error_found() is true")

        return dict(status="ERROR",\
                message=self.error_message)

    def get_http_err_code(self):
        """
        Return an HTTP status code usable in a JsonResponse object
        """
        if not self.was_error_found():
            raise AttributeError("Only call this if was_error_found() is true")

        return self.bad_http_status_code

    def get_error_msg_return(self):
        if not self.was_error_found():
            raise AttributeError("Only call this if was_error_found() is true")

        return False, self.error_message

    def load_dates_from_kwargs(self, **kwargs):
        """
        Accepts any, all or none of:

            start_date = YYYY-MM-DD
            end_date = YYYY-MM-DD
            selected_year = YYYY
            time_sort = a\d
        """
        # Add a start date, if it exists
        start_date_str = kwargs.get('start_date', None)
        if start_date_str is not None:
            convert_worked, self.start_date = format_yyyy_mm_dd(start_date_str)
            if not convert_worked:
                self.add_error('Start date is invalid.  Use YYYY-MM-DD format.', 400)
                return

        # Add an end date, if it exists
        end_date_str = kwargs.get('end_date', None)
        if end_date_str:
            convert_worked, self.end_date = format_yyyy_mm_dd(end_date_str)
            if not convert_worked:
                self.add_error('End date is invalid.  Use YYYY-MM-DD format.', 400)
                return

        # Sanity check: Make sure start date isn't after end date
        if self.start_date and self.end_date:   # do start and end dates exist
            if self.start_date > self.end_date: # sanity check
                self.add_error('The start date cannot be after the end date.', 400)
                return

        # Add a year, if it exists
        self.selected_year = kwargs.get('selected_year', None)
        if self.selected_year:
            if not (self.selected_year.isdigit() and len(self.selected_year) == 4):
                self.add_error('The year must be a 4-digit number (YYYY)a')
                return

        # Sanity check the selected_year and start_date
        if self.selected_year and self.start_date:
            if int(self.selected_year) < self.start_date.year:
                self.add_error("'The 'selected_year' (%s)"
                        "' cannot be before the 'start_date' year (%s)" %\
                            (self.selected_year, self.start_date.date()))
                return

        # Sanity check the selected_year and end_date
        if self.selected_year and self.end_date:
            if int(self.selected_year) > self.end_date.year:
                self.add_error("'The 'selected_year' (%s)"
                        "' cannot be after the 'end_date' year (%s)" %\
                            (self.selected_year, self.end_date.date()))
                return

        self.time_sort = str(kwargs.get('time_sort', ''))
        if self.time_sort == 'd':   # descending
            self.time_sort = '-'
        else:                       # ascending
            self.time_sort = ''


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

        if self.selected_year:
            filter_params['%s__year' % date_var_name] = self.selected_year

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

        # Retrieve the date parameters
        filter_params = self.get_date_filter_params()

        print 'filter_params', filter_params

        # add date filter
        ds_counts_by_month = Dataset.objects.filter(**filter_params)
        # add the rest of the filters
        ds_counts_by_month = ds_counts_by_month.annotate(\
            #month=TruncMonth('dvobject__createdate')\
            month_yyyy_dd=TruncYearMonth('dvobject__createdate')\
            ).values('month_yyyy_dd'\
            ).annotate(cnt=models.Count('dvobject_id')\
            ).values('month_yyyy_dd', 'cnt'\
            ).order_by('%smonth_yyyy_dd' % self.time_sort)

        running_total = 0
        for d in ds_counts_by_month:
            running_total += d['cnt']
            d['running_total'] = running_total
            d['year_num'] = int(d['month_yyyy_dd'][0:4])
            month_num = int(d['month_yyyy_dd'][5:])
            d['month_num'] = month_num
            month_name_found, month_name = get_month_name(month_num)
            if month_name_found:
                d['month_name'] = month_name
            else:
                # Log it!!!!!!
                pass
        return True, ds_counts_by_month
