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
    param_names = StatsViewSwagger.UNPUBLISHED_PARAMS + StatsViewSwagger.PRETTY_JSON_PARAM

    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""
        stats_files = StatsMakerFiles(**request.GET.dict())

        if self.is_published_and_unpublished(request):
            stats_result = stats_files.get_datafile_count()
        elif self.is_unpublished(request):
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

    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""
        stats_files = StatsMakerFiles(**request.GET.dict())

        if self.is_published_and_unpublished(request):
            stats_result = stats_files.get_file_count_by_month()
        elif self.is_unpublished(request):
            stats_result = stats_files.get_file_count_by_month_unpublished()
        else:
            stats_result = stats_files.get_file_count_by_month_published()

        return stats_result

class FilesDownloadedByMonthView(StatsViewSwagger):
    """API View - Downloaded Files counts by Month."""

    # Define the swagger attributes
    # Note: api_path must match the path in urls.py
    #
    api_path = '/files/downloads/count/monthly'
    summary = ('Number of downloaded Files by month')
    description = ('Returns a list of counts and'
            ' cumulative counts of all Files downloaded in a month')
    description_200 = 'A list of file download counts by month'

    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""
        stats_files = StatsMakerFiles(**request.GET.dict())

        if self.is_published_and_unpublished(request):
            stats_result = stats_files.get_file_downloads_by_month()
        elif self.is_unpublished(request):
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

    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""
        stats_files = StatsMakerFiles(**request.GET.dict())

        if self.is_published_and_unpublished(request):
            stats_result = stats_files.get_datafile_content_type_counts()
        elif self.is_unpublished(request):
            stats_result = stats_files.get_datafile_content_type_counts_unpublished()
        else:
            stats_result = stats_files.get_datafile_content_type_counts_published()

        return stats_result
