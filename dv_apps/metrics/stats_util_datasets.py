"""
Create metrics for Datasets.
This may be used for APIs, views with visualizations, etc.
"""

from django.shortcuts import render
from django.http import JsonResponse
#from django.db.models.functions import TruncMonth  # 1.10
from collections import OrderedDict
from django.db.models import Count
from django.db import models
from dv_apps.utils.date_helper import format_yyyy_mm_dd, get_month_name,\
    month_year_iterator
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


    def get_dataset_counts_by_create_date(self):

        return self.get_dataset_count_by_month(date_param='dvobject__createdate')


    def get_dataset_counts_by_publication_date(self):

        return self.get_dataset_count_by_month(date_param='dvobject__publicationdate')


    def get_dataset_count_by_month(self, date_param='dvobject__createdate'):
        """
        Return dataset counts by month
        """
        # Was an error found earlier?
        #
        if self.was_error_found():
            return self.get_error_msg_return()

        # -----------------------------------
        # (1) Build query filters
        # -----------------------------------

        # Exclude records where dates are null
        #   - e.g. a record may not have a publication date
        exclude_params = { '%s__isnull' % date_param : True}

        # Retrieve the date parameters
        #
        filter_params = self.get_date_filter_params()

        # -----------------------------------
        # (2) Construct query
        # -----------------------------------

        # add exclude filters date filters
        #
        ds_counts_by_month = Dataset.objects.select_related('dvobject'\
                            ).exclude(**exclude_params\
                            ).filter(**filter_params)

        # annotate query adding "month_yyyy_dd" and "cnt"
        #
        ds_counts_by_month = ds_counts_by_month.annotate(\
            month_yyyy_dd=TruncYearMonth('%s' % date_param)\
            ).values('month_yyyy_dd'\
            ).annotate(cnt=models.Count('dvobject_id')\
            ).values('month_yyyy_dd', 'cnt'\
            ).order_by('%smonth_yyyy_dd' % self.time_sort)

        # -----------------------------------
        # (3) Format results
        # -----------------------------------
        running_total = 0   # hold the running total count
        formatted_records = []  # move from a queryset to a []

        for d in ds_counts_by_month:
            # running total
            running_total += d['cnt']
            d['running_total'] = running_total

            # Add year and month numbers
            d['year_num'] = int(d['month_yyyy_dd'][0:4])
            month_num = int(d['month_yyyy_dd'][5:])
            d['month_num'] = month_num

            # Add month name
            month_name_found, month_name = get_month_name(month_num)
            if month_name_found:
                d['month_name'] = month_name
            else:
                # Log it!!!!!!
                pass

            # Add formatted record
            formatted_records.append(d)

        return True, formatted_records

    def make_month_lookup(self, stats_queryset):
        """Make a dict from the 'stats_queryset' with a key of YYYY-MMDD"""

        d = {}
        for info in stats_queryset:
            d[info['month_yyyy_dd']] = info
        return d


    def create_month_year_iterator(self, create_date_info, pub_date_info):
        """
        Get the range of create and pub dates
        """
        #import ipdb; ipdb.set_trace()
        if len(pub_date_info) == 0:
            # No pub date, return create date ranges
            if len(create_date_info) == 1:
                # create start/end dates are the same
                first_date = create_date_info[0]
                last_date = first_date
            elif len(create_date_info) > 1:
                # different start/end dates
                first_date = create_date_info[0]
                last_date = create_date_info[-1]
            else:
                # no start/end dates for pub date or create date
                return None   # No pub date or create date info
        else:
            # We have a pub date and a create date
            first_date = min([create_date_info[0], pub_date_info[0]])
            last_date = max([create_date_info[-1], pub_date_info[-1]])

        return month_year_iterator(first_date['year_num'],\
                            first_date['month_num'],\
                            last_date['year_num'],\
                            last_date['month_num'],\
                            )

    def get_dataset_counts_by_create_date_and_pub_date(self):
        """Combine create and publication date stats info"""

        if self.was_error_found():
            return self.get_error_msg_return()

        # (1) Get the stats for datasets *created* each month
        #
        success, create_date_info = self.get_dataset_counts_by_create_date()
        if not success:
            self.add_error('Failed to retrieve dataset counts by create date')

        # (2) Get the stats for datasets *published* each month
        #
        success, pub_date_info = self.get_dataset_counts_by_publication_date()
        if not success:
            self.add_error('Failed to retrieve dataset counts by publication date')

        # (3) Make dicts of these stats.  Key is YYYY-MMDD
        #
        create_date_dict = self.make_month_lookup(create_date_info)
        pub_date_dict = self.make_month_lookup(pub_date_info)

        # (4) Get list of months in YYYY-MMDD format to iterate through
        #
        month_iterator = self.create_month_year_iterator(create_date_info, pub_date_info)
        #import ipdb; ipdb.set_trace()
        #for yyyy, mm in
        #print 'pub_date_info', len(pub_date_info)

        #months_in_pub_only = set(pub_date_dict.keys()) - set(create_date_dict.keys())

        # Iterate through create_date_info
        formatted_dict = OrderedDict()
        formatted_list = []

        last_pub_running_total = 0
        for dataset_info in create_date_info:
            current_month = dataset_info['month_yyyy_dd']

            # Are there publication date numbers for this month?
            #
            pub_info = pub_date_dict.get(current_month, None)
            if pub_info:    # Yes, Add it to the create date dict
                dataset_info['pub_cnt'] = pub_info['cnt']
                dataset_info['pub_running_total'] = pub_info['running_total']
                last_pub_running_total = pub_info['running_total']
            else:           # No, Add last running total to the create date dict
                dataset_info['pub_cnt'] = 0    # No datasets published this month
                dataset_info['pub_running_total'] = last_pub_running_total

            formatted_dict[current_month] = dataset_info
            formatted_list.append(dataset_info)

        # NOT DONE - NEED TO CHECK for MISSING MONTHS ADD PUB ONLY MONTHS! by using month_iterator



        return True, formatted_list
