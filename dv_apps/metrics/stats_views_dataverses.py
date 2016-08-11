from .stats_view_base import StatsViewSwagger
from .stats_util_dataverses import StatsMakerDataverses


class DataverseCountByMonthView(StatsViewSwagger):
    """API View - Dataverse counts by Month."""

    # Define the swagger attributes
    #
    api_path = '/dataverses/count/monthly'
    summary = ('Number of published Dataverses by'
            ' the month they were created*.  (*'
            ' Not necessarily the same month they'
            ' were published)')
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

class DataverseTotalCounts(StatsViewSwagger):
    """API View - Total count of all Dataverses"""

    # Define the swagger attributes
    #
    api_path = '/dataverses/count'
    summary = ('Simple count of published Dataverses')
    description = ('Returns number of published Dataverses')
    description_200 = 'Number of published Dataverses'
    param_names = StatsViewSwagger.UNPUBLISHED_PARAMS + StatsViewSwagger.PRETTY_JSON_PARAM

    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""
        stats_datasets = StatsMakerDataverses(**request.GET.dict())

        if self.is_published_and_unpublished(request):
            stats_result = stats_datasets.get_dataverse_count()
        elif self.is_unpublished(request):
            stats_result = stats_datasets.get_dataverse_count_unpublished()
        else:
            stats_result = stats_datasets.get_dataverse_count_published()

        return stats_result

class DataverseAffiliationCounts(StatsViewSwagger):
    """API View - Number of Dataverses by Affiliation"""

    # Define the swagger attributes
    #
    api_path = '/dataverses/count/by-affiliation'
    summary = ('Number of Dataverses by Affiliation')
    description = ('Number of Dataverses by Affiliation.')
    description_200 = 'Number of published Dataverses by Affiliation.'
    param_names = StatsViewSwagger.UNPUBLISHED_PARAMS + StatsViewSwagger.PRETTY_JSON_PARAM

    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""
        stats_datasets = StatsMakerDataverses(**request.GET.dict())

        if self.is_published_and_unpublished(request):
            stats_result = stats_datasets.get_dataverse_affiliation_counts()
        elif self.is_unpublished(request):
            stats_result = stats_datasets.get_dataverse_affiliation_counts_unpublished()
        else:
            stats_result = stats_datasets.get_dataverse_affiliation_counts_published()

        return stats_result
