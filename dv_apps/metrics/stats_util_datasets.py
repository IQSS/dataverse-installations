"""
Create metrics for Datasets.
This may be used for APIs, views with visualizations, etc.
"""
#from django.db.models.functions import TruncMonth  # 1.10
from collections import OrderedDict
from django.db import models
from dv_apps.utils.date_helper import format_yyyy_mm_dd, get_month_name,\
    month_year_iterator
#from dv_apps.dvobjects.models import DvObject, DTYPE_DATASET
from dv_apps.datasets.models import Dataset
from dv_apps.datafiles.models import Datafile
from dv_apps.dataverses.models import Dataverse, DATAVERSE_TYPE_UNCATEGORIZED
from dv_apps.guestbook.models import GuestBookResponse, RESPONSE_TYPE_DOWNLOAD

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
                self.add_error('The year must be a 4-digit number (YYYY)')
                return
            if int(self.selected_year) < 0:
                self.add_error('The year must cannot be less than 1.')
            if int(self.selected_year) == 0:
                self.add_error('The year must cannot be zero.')

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

        # Optional time sort parameter
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


    def get_is_published_filter_param(self):

        return dict(dvobject__publicationdate__isnull=False)

    def get_is_NOT_published_filter_param(self):

        return dict(dvobject__publicationdate__isnull=True)

    # ----------------------------
    #  Datafile counts
    # ----------------------------
    def get_datafile_count(self, **extra_filters):
        """
        Return the Datafile count
        """
        if self.was_error_found():
            return self.get_error_msg_return()

        filter_params = self.get_date_filter_params()
        if extra_filters:
            for k, v in extra_filters.items():
                filter_params[k] = v

        return True, Datafile.objects.filter(**filter_params).count()

    def get_datafile_count_published(self):
        """
        Return the count of published Dataverses
        """
        return self.get_datafile_count(**self.get_is_published_filter_param())


    def get_datafile_count_unpublished(self):
        """
        Return the count of published Dataverses
        """
        return self.get_datafile_count(**self.get_is_NOT_published_filter_param())


    # ----------------------------
    #  Dataverse counts
    # ----------------------------
    def get_dataverse_count_published(self):
        """
        Return the count of published Dataverses
        """
        return self.get_dataverse_count(**self.get_is_published_filter_param())


    def get_dataverse_count_unpublished(self):
        """
        Return the count of unpublished Dataverses
        """
        return self.get_dataverse_count(**self.get_is_NOT_published_filter_param())


    def get_dataverse_count(self, **extra_filters):
        """
        Return the Dataverse count
        """
        if self.was_error_found():
            return self.get_error_msg_return()

        filter_params = self.get_date_filter_params()
        if extra_filters:
            for k, v in extra_filters.items():
                filter_params[k] = v

        return True, Dataverse.objects.filter(**filter_params).count()

    # ----------------------------
    #   Dataset counts (single number totals)
    # ----------------------------
    def get_dataset_count(self, **extra_filters):
        """
        Return the Dataset count
        """
        if self.was_error_found():
            return self.get_error_msg_return()

        filter_params = self.get_date_filter_params()
        if extra_filters:
            for k, v in extra_filters.items():
                filter_params[k] = v

        return True, Dataset.objects.filter(**filter_params).count()

    def get_dataset_count_published(self):
        """
        Return the count of published Dataverses
        """
        return self.get_dataverse_count(**self.get_is_published_filter_param())


    def get_dataset_count_unpublished(self):
        """
        Return the count of unpublished Dataverses
        """
        return self.get_dataverse_count(**self.get_is_NOT_published_filter_param())

    # ----------------------------
    #   Dataset counts by create date
    # ----------------------------
    def get_dataset_counts_by_create_date(self, **extra_filters):
        """
        Get # of datasets created each month
        """
        if self.was_error_found():
            return self.get_error_msg_return()

        filter_params = self.get_date_filter_params()
        if extra_filters:
            for k, v in extra_filters.items():
                filter_params[k] = v

        return self.get_dataset_count_by_month(date_param='dvobject__createdate')


    def get_dataset_counts_by_create_date_published(self):
        """
        Get # of --PUBLISHED-- datasets created each month
        """
        return self.get_dataset_counts_by_create_date(**self.get_is_published_filter_param())


    def get_dataset_counts_by_create_date_unpublished(self):
        """
        Get # of --UNPUBLISHED-- datasets created each month
        """
        return self.get_dataset_counts_by_create_date(**self.get_is_NOT_published_filter_param())


    def get_dataset_counts_by_publication_date(self):
        """
        Get # of datasets published each month
        """
        return self.get_dataset_count_by_month(date_param='dvobject__publicationdate')


    def get_dataset_counts_by_modification_date(self):
        """
        Get # of datasets modified each month

        Not great b/c only the last modified date is recorded
        """
        return self.get_dataset_count_by_month(date_param='dvobject__modificationtime')


    def get_dataset_count_by_month(self, date_param='dvobject__createdate', **extra_filters):
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

        # Add extra filters from kwargs
        #
        if extra_filters:
            for k, v in extra_filters.items():
                filter_params[k] = v

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

        #print (ds_counts_by_month)

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
        """INCOMPLETE - Combine create and publication date stats info"""

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

    def get_downloads_by_month(self):
        """
        Using the GuestBookResponse object, find the number of file
        downloads per month
        """
        if self.was_error_found():
            return self.get_error_msg_return()

        filter_params = self.get_date_filter_params(date_var_name='responsetime')
        filter_params['downloadtype'] = RESPONSE_TYPE_DOWNLOAD

        file_counts_by_month = GuestBookResponse.objects.filter(**filter_params\
            ).annotate(month_yyyy_dd=TruncYearMonth('responsetime')\
            ).values('month_yyyy_dd'\
            ).annotate(cnt=models.Count('guestbook_id')\
            ).values('month_yyyy_dd', 'cnt'\
            ).order_by('%smonth_yyyy_dd' % self.time_sort)

        formatted_records = []  # move from a queryset to a []
        file_running_total = 0
        for d in file_counts_by_month:
            file_running_total += d['cnt']
            d['running_total'] = file_running_total

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

            formatted_records.append(d)

        return True, formatted_records


    def get_dataverse_counts_by_type(self, uncategorized_replacement_name=None):
        """
        Return dataverse counts by 'dataversetype'

        Optional if a dataverse is uncategorized:
            - Specifying 'uncategorized_replacement_name' will
                set "UNCATEGORIZED" to another string

        Returns: { "dv_counts_by_type": [
                        {
                            "total_count": 356,
                            "dataversetype": "RESEARCH_PROJECTS",
                            "type_count": 85,
                            "percent_string": "23.9%"
                        },
                        {
                            "total_count": 356,
                            "dataversetype": "TEACHING_COURSES",
                            "type_count": 10,
                            "percent_string": "2.8%"
                        }
                            ... etc
                    ]
                }
        """
        if self.was_error_found():
            return self.get_error_msg_return()

        # Retrieve the date parameters
        #
        filter_params = self.get_date_filter_params('dvobject__createdate')

        dataverse_counts_by_type = Dataverse.objects.select_related('dvobject'\
                    ).filter(**filter_params\
                    ).values('dataversetype'\
                    ).annotate(type_count=models.Count('dataversetype'))

        # Count all dataverses
        #
        total_count = sum([rec.get('type_count', 0) for rec in dataverse_counts_by_type])
        total_count = total_count + 0.0

        # Format the records, adding 'total_count' and 'percent_string' to each one
        #
        formatted_records = []
        for rec in dataverse_counts_by_type:

            if total_count > 0:
                float_percent = rec.get('type_count', 0) / total_count
                rec['percent_string'] = '{0:.1%}'.format(float_percent)
                rec['total_count'] = int(total_count)

            # Optional: Add alternate name for DATAVERSE_TYPE_UNCATEGORIZED
            #
            if uncategorized_replacement_name:
                if rec['dataversetype'] == DATAVERSE_TYPE_UNCATEGORIZED:
                    rec['dataversetype'] = uncategorized_replacement_name

            formatted_records.append(rec)

        return True, formatted_records

    def get_dataverse_affiliation_counts(self):
        """
        Return dataverse counts by 'affiliation'

        Optional if a dataverse is uncategorized:
            - Specifying 'uncategorized_replacement_name' will
                set "UNCATEGORIZED" to another string

        Returns: { "dv_counts_by_type": [
                        {
                            "total_count": 356,
                            "dataversetype": "RESEARCH_PROJECTS",
                            "type_count": 85,
                            "percent_string": "23.9%"
                        },
                        {
                            "total_count": 356,
                            "dataversetype": "TEACHING_COURSES",
                            "type_count": 10,
                            "percent_string": "2.8%"
                        }
                            ... etc
                    ]
                }
        """
        if self.was_error_found():
            return self.get_error_msg_return()

        # Retrieve the date parameters
        #
        filter_params = self.get_date_filter_params('dvobject__createdate')

        dataverse_counts_by_affil = Dataverse.objects.select_related('dvobject'\
                    ).filter(**filter_params\
                    ).values('affiliation'\
                    ).annotate(affil_count=models.Count('affiliation'))

        # Count all dataverses
        #
        total_count = sum([rec.get('affil_count', 0) for rec in dataverse_counts_by_affil])
        total_count = total_count + 0.0

        # Format the records, adding 'total_count' and 'percent_string' to each one
        #
        formatted_records = []
        for rec in dataverse_counts_by_affil:

            if total_count > 0:
                float_percent = rec.get('affil_count', 0) / total_count
                rec['percent_string'] = '{0:.1%}'.format(float_percent)
                rec['total_count'] = int(total_count)

            # Optional: Add alternate name for DATAVERSE_TYPE_UNCATEGORIZED
            #
            #if uncategorized_replacement_name:
            #    if rec['dataversetype'] == DATAVERSE_TYPE_UNCATEGORIZED:
            #        rec['dataversetype'] = uncategorized_replacement_name

            formatted_records.append(rec)

        return True, formatted_records
