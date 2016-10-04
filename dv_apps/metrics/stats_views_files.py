from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from dv_apps.dataverse_auth.decorator import superuser_apikey_required
from dv_apps.utils.metrics_cache_time import get_metrics_api_cache_time

from .stats_view_base import StatsViewSwagger
from .stats_util_files import StatsMakerFiles

class FileTotalCountsView(StatsViewSwagger):
    """API View - Total count of all Files"""

    # Define the swagger attributes
    # Note: api_path must match the path in urls.py
    #
    api_path = '/files/count'
    summary = ('Simple count of published Files')
    description = ('Returns number of published Files')
    description_200 = 'Number of published Files'
    param_names = StatsViewSwagger.PARAM_DV_API_KEY + StatsViewSwagger.PUBLISH_PARAMS + StatsViewSwagger.PRETTY_JSON_PARAM
    result_name = StatsViewSwagger.RESULT_NAME_FILE_EXT_COUNTS
    tags = [StatsViewSwagger.TAG_DATAFILES]
    result_name = StatsViewSwagger.RESULT_NAME_TOTAL_COUNT

    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""
        stats_files = StatsMakerFiles(**request.GET.dict())

        pub_state = self.get_pub_state(request)

        if pub_state == self.PUB_STATE_ALL:
            stats_result = stats_files.get_datafile_count()
        elif pub_state == self.PUB_STATE_UNPUBLISHED:
            stats_result = stats_files.get_datafile_count_unpublished()
        else:
            stats_result = stats_files.get_datafile_count_published()

        return stats_result


class FileCountByMonthView(StatsViewSwagger):
    """API View - Published Files counts by Month.
    To do: Enforce permissions
    """

    # Define the swagger attributes
    # Note: api_path must match the path in urls.py
    #
    api_path = '/files/count/monthly'
    summary = ('Number of Files by'
            ' the month they were created*.  (*'
            ' Not month published)')
    description = ('Returns a list of counts and'
            ' cumulative counts of all Files added in a month')
    description_200 = 'A list of File counts by month'
    param_names = StatsViewSwagger.PARAM_DV_API_KEY +\
                StatsViewSwagger.BASIC_DATE_PARAMS +\
                StatsViewSwagger.PUBLISH_PARAMS +\
                StatsViewSwagger.PRETTY_JSON_PARAM +\
                StatsViewSwagger.PARAM_AS_CSV
    tags = [StatsViewSwagger.TAG_DATAFILES]

    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""
        stats_files = StatsMakerFiles(**request.GET.dict())

        pub_state = self.get_pub_state(request)

        if pub_state == self.PUB_STATE_ALL:
            stats_result = stats_files.get_file_count_by_month()
        elif pub_state == self.PUB_STATE_UNPUBLISHED:
            stats_result = stats_files.get_file_count_by_month_unpublished()
        else:
            stats_result = stats_files.get_file_count_by_month_published()

        return stats_result

@method_decorator(superuser_apikey_required, name='get')
@method_decorator(cache_page(get_metrics_api_cache_time()), name='get')
class FilesDownloadedByMonthView(StatsViewSwagger):
    """API View - Downloaded Files counts by Month."""

    # Define the swagger attributes
    # Note: api_path must match the path in urls.py
    #
    api_path = '/files/downloads/count/monthly'
    summary = ('Number of downloaded Files by month')
    description = ('Returns a list of counts and'
            ' cumulative counts of all Files downloaded in a month.'
            ' Superuser access required.')
    description_200 = 'A list of file download counts by month.'
    tags = [StatsViewSwagger.TAG_DATAFILES]

    param_names = StatsViewSwagger.PARAM_DV_API_KEY +\
                StatsViewSwagger.BASIC_DATE_PARAMS +\
                StatsViewSwagger.PUBLISH_PARAMS +\
                StatsViewSwagger.PRETTY_JSON_PARAM +\
                StatsViewSwagger.PARAM_SELECTED_DV_ALIASES +\
                StatsViewSwagger.PARAM_INCLUDE_CHILD_DVS +\
                StatsViewSwagger.PARAM_AS_CSV

    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""

        stats_files = StatsMakerFiles(**request.GET.dict())

        pub_state = self.get_pub_state(request)

        if pub_state == self.PUB_STATE_ALL:
            stats_result = stats_files.get_file_downloads_by_month()
        elif pub_state == self.PUB_STATE_UNPUBLISHED:
            stats_result = stats_files.get_file_downloads_by_month_unpublished()
        else:
            stats_result = stats_files.get_file_downloads_by_month_published()

        return stats_result



class FileCountsByContentTypeView(StatsViewSwagger):
    """API View - Files counts by content type."""

    # Define the swagger attributes
    # Note: api_path must match the path in urls.py
    #
    api_path = '/files/count/by-type'
    summary = ('Number of files by content type')
    description = ('Returns a list of file counts by content type')
    description_200 = 'A list of file counts by content type'
    param_names = StatsViewSwagger.PARAM_DV_API_KEY +\
            StatsViewSwagger.BASIC_DATE_PARAMS +\
            StatsViewSwagger.PUBLISH_PARAMS +\
            StatsViewSwagger.PRETTY_JSON_PARAM +\
            StatsViewSwagger.PARAM_AS_CSV

    result_name = StatsViewSwagger.RESULT_NAME_FILE_TYPE_COUNTS
    tags = [StatsViewSwagger.TAG_DATAFILES]

    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""
        stats_files = StatsMakerFiles(**request.GET.dict())

        pub_state = self.get_pub_state(request)

        if pub_state == self.PUB_STATE_ALL:
            stats_result = stats_files.get_datafile_content_type_counts()
        elif pub_state == self.PUB_STATE_UNPUBLISHED:
            stats_result = stats_files.get_datafile_content_type_counts_unpublished()
        else:
            stats_result = stats_files.get_datafile_content_type_counts_published()

        return stats_result


class FileExtensionsWithinContentType(StatsViewSwagger):
    """API View - Files counts by content type."""

    # Define the swagger attributes
    # Note: api_path must match the path in urls.py
    #
    api_path = '/files/extensions'
    summary = ('File extension counts within a given content type.')
    description = ('File extension counts within a given content type.')
    description_200 = ('File extension counts within a given content type.')
    param_names = StatsViewSwagger.PARAM_DV_API_KEY +\
                StatsViewSwagger.FILE_CONTENT_TYPE_PARAM +\
                StatsViewSwagger.PRETTY_JSON_PARAM +\
                StatsViewSwagger.PARAM_AS_CSV

    result_name = StatsViewSwagger.RESULT_NAME_FILE_EXT_COUNTS #+\
    tags = [StatsViewSwagger.TAG_DATAFILES]

    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""
        stats_files = StatsMakerFiles()

        ctype = self.get_content_type_param(request)
        if ctype is None:
            stats_result = stats_files.view_file_extensions_within_type(None)
        else:
            stats_result = stats_files.view_file_extensions_within_type(ctype)

        return stats_result
