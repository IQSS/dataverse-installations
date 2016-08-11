
from .stats_view_base import StatsViewSwagger
from .stats_util_datasets import StatsMakerDatasets
from .stats_util_dataverses import StatsMakerDataverses

class DatasetCountByMonthView(StatsViewSwagger):
    """API View - Published Dataset counts by Month"""

    # Define the swagger attributes
    #
    api_path = '/datasets/count/monthly'
    summary = ('Number of published Datasets by'
            ' the month they were created.*  (*'
            ' Not necessarily the same month they'
            ' were created)')
    description = ('Returns a list of counts and'
            ' cumulative counts of all datasts added in a month')
    description_200 = 'A list of Dataset counts by month'

    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""
        stats_datasets = StatsMakerDatasets(**request.GET.dict())

        if self.is_published_and_unpublished(request):
            stats_result = stats_datasets.get_dataset_counts_by_create_date()
        elif self.is_unpublished(request):
            stats_result = stats_datasets.get_dataset_counts_by_create_date_unpublished()
        else:
            stats_result = stats_datasets.get_dataset_counts_by_create_date_published()

        return stats_result

class DataverseCountByMonthView(StatsViewSwagger):
    """API View - Unpublished Dataverse counts by Month.
    To do: Enforce permissions
    """

    # Define the swagger attributes
    #
    api_path = '/dataverses/count/monthly'
    summary = ('Number of unpublished Dataverses by'
            ' the month they were created.*  (*'
            ' Not necessarily the same month they'
            ' were created)')
    description = ('Returns a list of counts and'
            ' cumulative counts of all Dataverses added in a month')
    description_200 = 'A list of Dataverse counts by month'

    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""
        stats_datasets = StatsMakerDataverses(**request.GET.dict())

        if self.is_published_and_unpublished(request):
            stats_result = stats_datasets.get_dataverse_counts_by_month()
        elif self.is_unpublished(request):
            stats_result = stats_datasets.get_dataverse_counts_by_month_unpublished()
        else:
            stats_result = stats_datasets.get_dataverse_counts_by_month_published()

        return stats_result
