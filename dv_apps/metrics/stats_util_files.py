"""
Create metrics for Datasets.
This may be used for APIs, views with visualizations, etc.
"""
from os.path import splitext
from collections import OrderedDict

from django.db import models

from dv_apps.utils.date_helper import get_month_name_abbreviation
from dv_apps.dvobjects.models import DvObject, DTYPE_DATAFILE
from dv_apps.datafiles.models import Datafile, FileMetadata
from dv_apps.guestbook.models import GuestBookResponse, RESPONSE_TYPE_DOWNLOAD
from dv_apps.metrics.stats_util_base import StatsMakerBase, TruncYearMonth
from dv_apps.metrics.stats_result import StatsResult
from dv_apps.dvobjects.models import DVOBJECT_CREATEDATE_ATTR

FILE_TYPE_OCTET_STREAM = 'application/octet-stream'

class StatsMakerFiles(StatsMakerBase):

    def __init__(self, **kwargs):
        """
        Start and end dates are optional.

        start_date = string in YYYY-MM-DD format
        end_date = string in YYYY-MM-DD format
        """
        super(StatsMakerFiles, self).__init__(**kwargs)

    # ----------------------------
    #  Datafile counts - single number
    # ----------------------------
    def get_datafile_count(self, **extra_filters):
        """
        Return the Datafile count
        """
        if self.was_error_found():
            return self.get_error_msg_return()

        filter_params = self.get_date_filter_params()

        # Add extra filters, if they exist
        if extra_filters:
            for k, v in extra_filters.items():
                filter_params[k] = v

        q = Datafile.objects.filter(**filter_params)
        sql_query = str(q.query)

        return StatsResult.build_success_result(q.count(), sql_query)
        #    return True, Datafile.objects.filter(**filter_params).count()

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
    #  Monthly download counts
    # ----------------------------
    def get_file_downloads_by_month_published(self):
        """File downloads by month for published files"""

        params = self.get_is_published_filter_param(dvobject_var_name='datafile')

        return self.get_file_downloads_by_month(**params)

    def get_file_downloads_by_month_unpublished(self):
        """File downloads by month for unpublished files"""

        params = self.get_is_NOT_published_filter_param(dvobject_var_name='datafile')

        return self.get_file_downloads_by_month(**params)


    def get_file_download_start_point(self, **extra_filters):
        """Get the startpoint when keeping a running total of file downloads"""

        start_point_filters = self.get_running_total_base_date_filters(date_var_name='responsetime')
        if start_point_filters is None:
            return 0

        start_point_filters.update(self.get_download_type_filter())

        if extra_filters:
            for k, v in extra_filters.items():
                start_point_filters[k] = v

        q = GuestBookResponse.objects.filter(**start_point_filters)
        sql_query = str(q.query)

        return q.count()


    def get_download_type_filter(self):
        return {}
        #return dict(downloadtype=RESPONSE_TYPE_DOWNLOAD)


    def get_file_downloads_by_month(self, **extra_filters):
        """
        Using the GuestBookResponse object, find the number of file
        downloads per month
        """
        if self.was_error_found():
            return self.get_error_msg_return()

        filter_params = self.get_date_filter_params(date_var_name='responsetime')
        filter_params.update(self.get_download_type_filter())

        # Add extra filters, if they exist
        if extra_filters:
            for k, v in extra_filters.items():
                filter_params[k] = v

        file_counts_by_month = GuestBookResponse.objects.filter(**filter_params\
            ).annotate(yyyy_mm=TruncYearMonth('responsetime')\
            ).values('yyyy_mm'\
            ).annotate(cnt=models.Count('id')\
            ).values('yyyy_mm', 'cnt'\
            ).order_by('%syyyy_mm' % self.time_sort)

        #print 'file_counts_by_month.query', file_counts_by_month.query
        sql_query = str(file_counts_by_month.query)

        formatted_records = []  # move from a queryset to a []
        file_running_total = self.get_file_download_start_point(**extra_filters)

        for d in file_counts_by_month:
            file_running_total += d['cnt']
            d['running_total'] = file_running_total

            # d['month_year'] = d['yyyy_mm'].strftime('%Y-%m')

            # Add year and month numbers
            d['year_num'] = d['yyyy_mm'].year
            d['month_num'] = d['yyyy_mm'].month

            # Add month name
            month_name_found, month_name = get_month_name_abbreviation( d['yyyy_mm'].month)
            if month_name_found:
                d['month_name'] = month_name
            else:
                # Log it!!!!!!
                pass

            # change the datetime object to a string
            d['yyyy_mm'] = d['yyyy_mm'].strftime('%Y-%m')

            formatted_records.append(d)

        return StatsResult.build_success_result(formatted_records, sql_query)

        #return True, formatted_records


    # ----------------------------
    #  Monthly files added
    # ----------------------------
    def get_file_count_by_month_published(self):
        """Published file counts by month"""

        return self.get_file_count_by_month(**self.get_is_published_filter_param())

    def get_file_count_by_month_unpublished(self):
        """Unpublished file counts by month"""

        return self.get_file_count_by_month(**self.get_is_NOT_published_filter_param())

        #params = self.get_is_NOT_published_filter_param(dvobject_var_name='datafile')

        #return self.get_file_downloads_by_month(**params)
        #return self.get_file_downloads_by_month(**self.get_is_NOT_published_filter_param())


    def get_file_count_start_point(self, **extra_filters):
        """Get the startpoint when keeping a running total of file downloads"""

        start_point_filters = self.get_running_total_base_date_filters()
        if start_point_filters is None:
            return 0

        if extra_filters:
            for k, v in extra_filters.items():
                start_point_filters[k] = v

        return Datafile.objects.select_related('dvobject').filter(**start_point_filters).count()


    def get_file_count_by_month(self, date_param=DVOBJECT_CREATEDATE_ATTR, **extra_filters):
        """
        File counts by month
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
        if date_param == DVOBJECT_CREATEDATE_ATTR:
            exclude_params = {}
        else:
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
        file_counts_by_month = Datafile.objects.select_related('dvobject'\
                            ).exclude(**exclude_params\
                            ).filter(**filter_params)

        # annotate query adding "month_year" and "cnt"
        #
        file_counts_by_month = file_counts_by_month.annotate(\
            yyyy_mm=TruncYearMonth('%s' % date_param)\
            ).values('yyyy_mm'\
            ).annotate(cnt=models.Count('dvobject_id')\
            ).values('yyyy_mm', 'cnt'\
            ).order_by('%syyyy_mm' % self.time_sort)

        sql_query = str(file_counts_by_month.query)

        # -----------------------------------
        # (3) Format results
        # -----------------------------------
        running_total = self.get_file_count_start_point(**extra_filters)   # hold the running total count
        formatted_records = []  # move from a queryset to a []

        for d in file_counts_by_month:
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

        #return True, formatted_records


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

    # ----------------------------
    #  Datafile counts by content type.
    #   e.g. how many .csv files, how many excel files, etc.
    # ----------------------------

    def get_datafile_content_type_counts_published(self):
        """Return datafile counts by 'content type' for published files"""

        return self.get_datafile_content_type_counts(\
            **self.get_is_published_filter_param())

    def get_datafile_content_type_counts_unpublished(self):
        """Return datafile counts by 'content type' for unpublished files"""

        return self.get_datafile_content_type_counts(\
            **self.get_is_NOT_published_filter_param())

    def get_datafile_content_type_counts(self, **extra_filters):
        """
        Return datafile counts by 'content type'

        "datafile_content_type_counts": [
                {
                    "total_count": 1584,
                    "contenttype": "text/tab-separated-values",
                    "type_count": 187,
                    "percent_string": "11.8%"
                },
                {
                    "total_count": 1584,
                    "contenttype": "image/jpeg",
                    "type_count": 182,
                    "percent_string": "11.5%"
                },
                {
                    "total_count": 1584,
                    "contenttype": "text/plain",
                    "type_count": 147,
                    "percent_string": "9.3%"
                }
            ]
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

        datafile_counts_by_type = Datafile.objects.select_related('dvobject'\
                    ).filter(**filter_params\
                    ).values('contenttype'\
                    ).order_by('contenttype'\
                    ).annotate(type_count=models.Count('contenttype')\
                    ).order_by('-type_count')

        sql_query = str(datafile_counts_by_type.query)

        # Count all dataverses
        #
        total_count = sum([rec.get('type_count', 0) for rec in datafile_counts_by_type])
        total_count = total_count + 0.0

        # Format the records, adding 'total_count' and 'percent_string' to each one
        #
        formatted_records = []
        #num = 0
        for rec in datafile_counts_by_type:

            if total_count > 0:
                float_percent = rec.get('type_count', 0) / total_count
                rec['percent_string'] = '{0:.1%}'.format(float_percent)
                rec['total_count'] = int(total_count)

                contenttype_parts = rec['contenttype'].split('/')
                if len(contenttype_parts) > 1:
                    rec['short_content_type'] = '/'.join(contenttype_parts[1:])
                else:
                    rec['short_content_type'] = rec['contenttype']
                #num+=1
                #rec['num'] = num
            formatted_records.append(rec)

        return StatsResult.build_success_result(formatted_records, sql_query)


    def get_files_per_dataset(self):
        """
        To do.....
        """

        # Pull file counts under each dataset
        files_per_dataset = DvObject.objects.filter(dtype=DTYPE_DATAFILE\
                    ).filter(**filter_params\
                    ).values('owner'\
                    ).annotate(parent_count=models.Count('owner')\
                    ).order_by('-parent_count')

        # Bin this data


    def view_file_extensions_within_type(self, file_type=None):
        """View extensions for files based on their "Filemetadata.contenttype" value"""

        #file_type = 'data/various-formats'

        if file_type is None:
            # Retrieve list of **all** file names -- this could be too much!
            l = FileMetadata.objects.all().values_list('label', flat=True)
        else:
            # Retrieve ids of Datafile filtered by "contenttype"
            ids = Datafile.objects.filter(contenttype=file_type).values_list('dvobject__id', flat=True)

            # Retrieve the names of these Datafiles via the FileMetadata object
            l = FileMetadata.objects.filter(datafile__in=ids).values_list('label', flat=True)

        # Convert the file names to file extensions
        ext_list = [splitext(label)[-1] for label in l]

        # Make a dict counting the extensions
        extension_counts = {}   # {file extension : count, file ext : count, etc}
        for ext in ext_list:
            extension_counts[ext] = extension_counts.get(ext, 0) + 1

        # Sort the counts in descending order--highest count first
        ext_pairs = extension_counts.items()
        ext_pairs = sorted(ext_pairs, key=lambda k: k[1], reverse=True)

        ext_list = []
        total_count = sum(x[1] for x in ext_pairs) + 0.000
        for ext_pair in ext_pairs:
            d = OrderedDict(extension=ext_pair[0])
            d['count'] = ext_pair[1]
            d['total_count'] = int(total_count)
            d['percent_string'] = '{0:.3%}'.format(ext_pair[1] / total_count)
            ext_list.append(d)

        d = OrderedDict(number_unique_extensions=len(ext_pairs))
        d['file_extension_counts'] = ext_list

        return StatsResult.build_success_result(d)

        #return JsonResponse(d)
