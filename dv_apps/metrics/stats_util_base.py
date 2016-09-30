"""
Create metrics for Datasets.
This may be used for APIs, views with visualizations, etc.
"""
#from django.db.models.functions import TruncMonth  # 1.10
from django.db import models

from dv_apps.utils.date_helper import format_yyyy_mm_dd
from dv_apps.dvobjects.models import DVOBJECT_CREATEDATE_ATTR
from dv_apps.metrics.stats_result import StatsResult
from dv_apps.metrics.dataverse_tree_util import DataverseTreeUtil

class TruncMonth(models.Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()

class xTruncYearMonth(models.Func):
    function = 'to_char'
    template = "%(function)s(%(expressions)s, 'YYYY-MM')"
    output_field = models.CharField()

class TruncYearMonth(models.Func):
    function = 'date_trunc'
    template = "%(function)s('month',%(expressions)s)"
    output_field = models.DateTimeField()


#select date_trunc('month', responsetime) as mth, count(id) from guestbookresponse group by mth;
    #to_char(createdate, 'YYYY-MM')

class StatsMakerBase(object):

    DEFAULT_BIN_SIZE = 20

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

        # Next 3 are currently only for file downloads
        self.selected_dvs = None    # Narrow by dataverse aliases
        self.include_child_dvs  = None

        # Used for binning stats
        self.bin_size = 20      # default setting
        self.num_bins = None    # optional setting
        self.skip_empty_bins = False

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

        return StatsResult.build_error_result(self.error_message,\
            self.bad_http_status_code)


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
        if isinstance(self.selected_year, (int, long)):
            # convert back to a string for err checking, etc
            self.selected_year = '%s' % self.selected_year
            self.selected_year = self.selected_year.zfill(4)

        if self.selected_year:
            if not self.selected_year.isdigit():
                self.add_error('The year must be digits.')
                return
            if not (self.selected_year.isdigit() and len(self.selected_year) == 4):
                self.add_error('The year cannot be more than 4-digits (YYYY)')
                return
            if int(self.selected_year) < 0:
                self.add_error('The year must cannot be less than 1.')
                return
            if int(self.selected_year) == 0:
                self.add_error('The year cannot be zero.')
                return

        # Sanity check the selected_year and start_date
        if self.selected_year and self.start_date:
            if int(self.selected_year) < self.start_date.year:
                self.add_error("The 'selected_year' (%s)"
                        "' cannot be before the 'start_date' year (%s)" %\
                            (self.selected_year, self.start_date.date()))
                return

        # Sanity check the selected_year and end_date
        if self.selected_year and self.end_date:
            if int(self.selected_year) > self.end_date.year:
                self.add_error("The 'selected_year' (%s)"
                        "' cannot be after the 'end_date' year (%s)" %\
                            (self.selected_year, self.end_date.date()))
                return

        # Optional time sort parameter
        self.time_sort = str(kwargs.get('time_sort', ''))
        if self.time_sort == 'd':   # descending
            self.time_sort = '-'
        elif self.time_sort in ['a', '']:   # ascending
            self.time_sort = ''
        else:                       # ascending
            self.add_error("'The 'time_sort' value"
                " must be 'a' for ascending or 'd' for descending.")
            return

        # ----------------------------------------
        # Optional: selected dataverse aliases
        #   - 8/31: Only used for file downloads
        # ----------------------------------------
        self.selected_dvs = kwargs.get('selected_dvs', None)
        if self.selected_dvs is not None:
            # make dvs into a list, stripping whitespace from each one
            self.selected_dvs = [x.strip() for x in self.selected_dvs.strip().split(',')]
            self.selected_dvs = [x for x in self.selected_dvs if len(x) > 0]
            if len(self.selected_dvs) == 0:
                self.selected_dvs = None

        # ----------------------------------------
        # Related to above: option to include child Dataverses
        # ----------------------------------------
        self.include_child_dvs = self.get_param_true_false_value_via_kwargs(kwargs, 'include_child_dvs')


        # ----------------------------------------
        # Bin Size
        # ----------------------------------------
        self.bin_size = kwargs.get('bin_size', self.DEFAULT_BIN_SIZE)
        self.bin_size = self.check_param_that_must_be_integer('bin_size', self.bin_size, none_ok=True)

        # ----------------------------------------
        # Number of bins
        # ----------------------------------------
        self.num_bins = kwargs.get('num_bins', None)
        self.num_bins = self.check_param_that_must_be_integer('num_bins', self.num_bins, none_ok=True)

        # ----------------------------------------
        # Skip empty bins?
        # ----------------------------------------
        self.skip_empty_bins = self.get_param_true_false_value_via_kwargs(kwargs, 'skip_empty_bins')

    def get_param_true_false_value_via_kwargs(self, kwarg_dict, param_name):
        assert kwarg_dict is not None, "kwarg_dict cannot be None"

        param_val = kwarg_dict.get(param_name, False)

        return self.get_param_true_false_value(param_val)


    @staticmethod
    def is_param_value_true(param_val):
        if param_val is None:
            return False

        if param_val in (True, 'True', 'true'):
            return True

        return False

    def get_param_true_false_value(self, param_val):

        return StatsMakerBase.is_param_value_true(param_val)


    def check_param_that_must_be_integer(self, param_name, param_value, none_ok=True):
        """Checking for several params that should be integers but may
        arrive as string, long, or int

        In this check, None is ok!
        """
        if not param_value:
            if none_ok:
                return None
            else:
                self.add_error("This parameter is required: %s" % param_name)
                return None

        # May come in as a string. If it's int or long, make it a string to check
        if isinstance(param_value, (int, long)):
            param_value = '%s' % param_value

        if not param_value.isdigit():
            self.add_error('The "%s" must a number.' % param_name)
            return None

        param_value = int(param_value)
        if param_value < 1:
            self.add_error('The "%s" must 1 or greater.' % param_name)
            return None

        return int(param_value)
        # OK, keep going

    def get_selected_dataverse_ids(self):
        """From a list of aliases, return a list of dataverse ids"""
        if self.selected_dvs is None:
            return True, None

        if self.include_child_dvs is True:
            # don't include child dvs
            success, ids_or_msg = DataverseTreeUtil().get_selected_dataverse_ids(self.selected_dvs,\
                                    include_child_dvs=True)

        else:
            # include child dvs
            success, ids_or_msg = DataverseTreeUtil().get_selected_dataverse_ids(self.selected_dvs,\
                                    include_child_dvs=False)

        if not success:
            self.add_error(ids_or_msg)
            return False, ids_or_msg

        return success, ids_or_msg

    def get_running_total_base_date_filters(self, date_var_name=DVOBJECT_CREATEDATE_ATTR):
        """If we have a running total, get the start point filters"""
        filter_params = {}
        if self.start_date:
            filter_params['%s__lt' % date_var_name] = self.start_date

        if self.selected_year:
            filter_params['%s__year__lt' % date_var_name] = self.selected_year

        if len(filter_params) == 0:
            return None

        return filter_params


    def get_date_filter_params(self, date_var_name=DVOBJECT_CREATEDATE_ATTR):
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


    def get_is_published_filter_param(self, dvobject_var_name='dvobject'):
        """
        Check if the dvobject has a publication date--which indicates
        that it has been published
        """
        date_var = '%s__publicationdate__isnull' % dvobject_var_name
        return {date_var : False}


    def get_is_NOT_published_filter_param(self, dvobject_var_name='dvobject'):
        """
        Check if the dvobject has a null publication date--which indicates
        that it has NOT been published
        """
        date_var = '%s__publicationdate__isnull' % dvobject_var_name
        return {date_var : True}
