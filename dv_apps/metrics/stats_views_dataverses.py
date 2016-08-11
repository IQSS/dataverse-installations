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


class DataverseTypeCounts(StatsViewSwagger):

    # Define the swagger attributes
    #
    api_path = '/dataverses/count/by-type'
    summary = ('Number of Dataverses by Type')
    description = ('Number of Dataverses by Type.')
    description_200 = 'Number of published Dataverses by Type.'
    param_names = StatsViewSwagger.UNPUBLISHED_PARAMS +\
                    StatsViewSwagger.PRETTY_JSON_PARAM +\
                    StatsViewSwagger.DV_TYPE_UNCATEGORIZED_PARAM

    def is_show_uncategorized(self, request):
        """Return the result of the "?show_uncategorized" query string param"""

        show_uncategorized = request.GET.get('show_uncategorized', False)
        if show_uncategorized is True or show_uncategorized == 'true':
            return True
        return False


    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""
        stats_datasets = StatsMakerDataverses(**request.GET.dict())

        if self.is_show_uncategorized(request):
            exclude_uncategorized = False
        else:
            exclude_uncategorized = True

        if self.is_published_and_unpublished(request):
            stats_result = stats_datasets.get_dataverse_counts_by_type(exclude_uncategorized)
        elif self.is_unpublished(request):
            stats_result = stats_datasets.get_dataverse_counts_by_type_unpublished(exclude_uncategorized)
        else:
            stats_result = stats_datasets.get_dataverse_counts_by_type_published(exclude_uncategorized)

        return stats_result
