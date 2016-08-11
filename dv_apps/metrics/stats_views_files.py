from .stats_view_base import StatsViewSwagger
from .stats_util_files import StatsMakerFiles


class FileCountByMonthView(StatsViewSwagger):
    """API View - Published Files counts by Month.
    To do: Enforce permissions
    """

    # Define the swagger attributes
    #
    api_path = '/files/count/monthly'
    summary = ('Number of unpublished Files by'
            ' the month they were created*.  (*'
            ' Not necessarily the same month they'
            ' were published)')
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
