"""
Create metrics for Dataverses.
This may be used for APIs, views with visualizations, etc.
"""
from django.db import models

from dv_apps.utils.date_helper import get_month_name_abbreviation
from dv_apps.dataverses.models import Dataverse, DATAVERSE_TYPE_UNCATEGORIZED
from dv_apps.metrics.stats_util_base import StatsMakerBase, TruncYearMonth
from dv_apps.metrics.stats_result import StatsResult
from dv_apps.dvobjects.models import DVOBJECT_CREATEDATE_ATTR
from dv_apps.harvesting.models import HarvestingDataverseConfig

class StatsMakerDataverses(StatsMakerBase):
    """
    Utility class to create stats for Dataverses
    """
    def __init__(self, **kwargs):
        """
        Start and end dates are optional.

        start_date = string in YYYY-MM-DD format
        end_date = string in YYYY-MM-DD format
        """
        super(StatsMakerDataverses, self).__init__(**kwargs)

        # Default to include harvested Dataverses
        # Note!  To really work, this logic needs to be applied to
        #   Datasets, Datafiles, etc.
        self.include_harvested = kwargs.get('include_harvested', True)

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
        Return the Dataverse count -- a single number
        """
        if self.was_error_found():
            return self.get_error_msg_return()

        filter_params = self.get_date_filter_params()
        if extra_filters:
            for k, v in extra_filters.items():
                filter_params[k] = v

        if self.include_harvested:
            q = Dataverse.objects.filter(**filter_params)
        else:
            q = Dataverse.objects.filter(**filter_params\
                    ).exclude(self.get_harvested_dataverse_ids()\
                    )

        sql_query = str(q.query)

        return StatsResult.build_success_result(q.count(), sql_query)


    # ----------------------------
    #  Dataverse counts by month
    # ----------------------------
    def get_dataverse_counts_by_month_unpublished(self):
        """
        Get # of --UNPUBLISHED-- datasets created each month
        """
        return self.get_dataverse_counts_by_month(**self.get_is_NOT_published_filter_param())


    def get_dataverse_counts_by_month_published(self):
        """
        Get # of --UNPUBLISHED-- datasets created each month
        """
        return self.get_dataverse_counts_by_month(**self.get_is_published_filter_param())


    def get_dataverse_count_start_point(self, **extra_filters):
        """Get the startpoint when keeping a running total of file downloads"""

        start_point_filters = self.get_running_total_base_date_filters()
        if start_point_filters is None:
            return 0

        if extra_filters:
            for k, v in extra_filters.items():
                start_point_filters[k] = v

        exclude_params = {}
        if self.include_harvested:
            exclude_params['dvobject__id__in'] = self.get_harvested_dataverse_ids()

        return Dataverse.objects.select_related('dvobject').filter(**start_point_filters).exclude(**exclude_params).count()

    def get_harvested_dataverse_ids(self):
        """Return the ids of harvested Dataverses"""

        return HarvestingDataverseConfig.objects.values_list('dataverse__id'\
                , flat=True).all()

    def get_dataverse_counts_by_month(self, date_param=DVOBJECT_CREATEDATE_ATTR, **extra_filters):
        """
        Return Dataverse counts by month
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
        if self.include_harvested:
            exclude_params['dvobject__id__in'] = self.get_harvested_dataverse_ids()

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
        dv_counts_by_month = Dataverse.objects.select_related('dvobject'\
                            ).exclude(**exclude_params\
                            ).filter(**filter_params)

        # annotate query adding "month_year" and "cnt"
        #
        dv_counts_by_month = dv_counts_by_month.annotate(\
            yyyy_mm=TruncYearMonth('%s' % date_param)\
            ).values('yyyy_mm'\
            ).annotate(cnt=models.Count('dvobject_id')\
            ).values('yyyy_mm', 'cnt'\
            ).order_by('%syyyy_mm' % self.time_sort)


        # -----------------------------------
        # (2a) Get SQL query string
        # -----------------------------------
        sql_query = str(dv_counts_by_month.query)

        # -----------------------------------
        # (3) Format results
        # -----------------------------------
        # hold the running total count
        running_total = self.get_dataverse_count_start_point(**extra_filters)
        formatted_records = []  # move from a queryset to a []

        for d in dv_counts_by_month:
            # running total
            running_total += d['cnt']
            d['running_total'] = running_total
            # d['month_year'] = d['yyyy_mm'].strftime('%Y-%m')

            # Add year and month numbers
            d['year_num'] = d['yyyy_mm'].year
            d['month_num'] = d['yyyy_mm'].month

            # Add month name
            month_name_found, month_name = get_month_name_abbreviation(d['yyyy_mm'].month)
            if month_name_found:
                d['month_name'] = month_name
            else:
                # Log it!!!!!!
                pass

            # change the datetime object to a string
            d['yyyy_mm'] = d['yyyy_mm'].strftime('%Y-%m')

            # Add formatted record
            formatted_records.append(d)

        return StatsResult.build_success_result(formatted_records, sql_query)


    def get_dataverse_counts_by_type_published(self, exclude_uncategorized=True):
        """Return dataverse counts by 'dataversetype' for published dataverses"""

        return self.get_dataverse_counts_by_type(exclude_uncategorized,\
                **self.get_is_published_filter_param())


    def get_dataverse_counts_by_type_unpublished(self, exclude_uncategorized=True):
        """Return dataverse counts by 'dataversetype' for unpublished dataverses"""

        return self.get_dataverse_counts_by_type(exclude_uncategorized,\
                **self.get_is_NOT_published_filter_param())


    def get_dataverse_counts_by_type(self, exclude_uncategorized=True, **extra_filters):
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
        filter_params = self.get_date_filter_params(DVOBJECT_CREATEDATE_ATTR)

        # Add extra filters
        if extra_filters:
            for k, v in extra_filters.items():
                filter_params[k] = v

        if exclude_uncategorized:
            exclude_params = dict(dataversetype=DATAVERSE_TYPE_UNCATEGORIZED)
        else:
            exclude_params = {}

        dataverse_counts_by_type = Dataverse.objects.select_related('dvobject'\
                    ).filter(**filter_params\
                    ).exclude(**exclude_params\
                    ).values('dataversetype'\
                    ).order_by('dataversetype'\
                    ).annotate(type_count=models.Count('dataversetype')\
                    ).order_by('-type_count')

        # -----------------------------------
        # Get SQL query string
        # -----------------------------------
        sql_query = str(dataverse_counts_by_type.query)

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

            rec['dataversetype_label'] = rec['dataversetype'].replace('_', ' ')

            formatted_records.append(rec)

        return StatsResult.build_success_result(formatted_records, sql_query)


    def get_dataverse_affiliation_counts(self):
        """
        Return dataverse counts by 'affiliation'

        Returns: dv_counts_by_affiliation": [
            {
                "affiliation": "University of Oxford",
                "affil_count": 2,
                "total_count": 191,
                "percent_string": "1.0%"
            },
            {
                "affiliation": "University of Illinois",
                "affil_count": 1,
                "total_count": 191,
                "percent_string": "0.5%"
            }
            ...
        ]
        """
        if self.was_error_found():
            return self.get_error_msg_return()

        # Retrieve the date parameters
        #
        filter_params = self.get_date_filter_params(DVOBJECT_CREATEDATE_ATTR)

        dataverse_counts_by_affil = Dataverse.objects.select_related('dvobject'\
                    ).filter(**filter_params\
                    ).values('affiliation'\
                    ).order_by('affiliation'\
                    ).annotate(affil_count=models.Count('affiliation')\
                    ).order_by('-affil_count')

        # -----------------------------------
        # Get SQL query string
        # -----------------------------------
        sql_query = str(dataverse_counts_by_affil.query)

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

            formatted_records.append(rec)

        return StatsResult.build_success_result(formatted_records, sql_query)

    '''
    def get_number_of_datafile_types(self):
        """Return the number of distinct contenttypes found in Datafile objects"""
        if self.was_error_found():
            return self.get_error_msg_return()

        # Retrieve the date parameters
        #
        filter_params = self.get_date_filter_params(DVOBJECT_CREATEDATE_ATTR)

        datafile_counts_by_type = Datafile.objects.select_related('dvobject'\
                    ).filter(**filter_params\
                    ).values('contenttype'\
                    ).distinct().count()

        return True, dict(datafile_counts_by_type=datafile_counts_by_type)
    '''
