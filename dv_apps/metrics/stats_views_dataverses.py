from .stats_view_base import StatsViewSwagger
from .stats_util_dataverses import StatsMakerDataverses


class DataverseCountByMonthView(StatsViewSwagger):
    """API View - Dataverse counts by Month."""

    # Define the swagger attributes
    # Note: api_path must match the path in urls.py
    #
    api_path = '/dataverses/count/monthly'
    summary = ('Number of published Dataverses by'
            ' the month they were created*.  (*'
            ' Not month published)')
    description = ('Returns a list of counts and'
            ' cumulative counts of all Dataverses added in a month')
    description_200 = 'A list of Dataverse counts by month'

    param_names = StatsViewSwagger.PARAM_DV_API_KEY +\
                StatsViewSwagger.BASIC_DATE_PARAMS +\
                StatsViewSwagger.PUBLISH_PARAMS +\
                StatsViewSwagger.PRETTY_JSON_PARAM +\
                StatsViewSwagger.PARAM_AS_CSV

    tags = [StatsViewSwagger.TAG_DATAVERSES]

    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""
        stats_datasets = StatsMakerDataverses(**request.GET.dict())

        pub_state = self.get_pub_state(request)

        if pub_state == self.PUB_STATE_ALL:
            stats_result = stats_datasets.get_dataverse_counts_by_month()
        elif pub_state == self.PUB_STATE_UNPUBLISHED:
            stats_result = stats_datasets.get_dataverse_counts_by_month_unpublished()
        else:
            stats_result = stats_datasets.get_dataverse_counts_by_month_published()

        return stats_result

class DataverseTotalCounts(StatsViewSwagger):
    """API View - Total count of all Dataverses"""

    # Define the swagger attributes
    # Note: api_path must match the path in urls.py
    #
    api_path = '/dataverses/count'
    summary = ('Simple count of published Dataverses')
    description = ('Returns number of published Dataverses')
    description_200 = 'Number of published Dataverses'
    param_names = StatsViewSwagger.PARAM_DV_API_KEY + StatsViewSwagger.PUBLISH_PARAMS + StatsViewSwagger.PRETTY_JSON_PARAM
    tags = [StatsViewSwagger.TAG_DATAVERSES]
    result_name = StatsViewSwagger.RESULT_NAME_TOTAL_COUNT


    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""
        stats_datasets = StatsMakerDataverses(**request.GET.dict())

        pub_state = self.get_pub_state(request)

        if pub_state == self.PUB_STATE_ALL:
            stats_result = stats_datasets.get_dataverse_count()
        elif pub_state == self.PUB_STATE_UNPUBLISHED:
            stats_result = stats_datasets.get_dataverse_count_unpublished()
        else:
            stats_result = stats_datasets.get_dataverse_count_published()

        return stats_result


class DataverseAffiliationCounts(StatsViewSwagger):
    """API View - Number of Dataverses by Affiliation"""

    # Define the swagger attributes
    # Note: api_path must match the path in urls.py
    #
    api_path = '/dataverses/count/by-affiliation'
    summary = ('Number of Dataverses by Affiliation')
    description = ('Number of Dataverses by Affiliation.')
    description_200 = 'Number of published Dataverses by Affiliation.'
    param_names = StatsViewSwagger.PARAM_DV_API_KEY + StatsViewSwagger.PUBLISH_PARAMS + StatsViewSwagger.PRETTY_JSON_PARAM
    result_name = StatsViewSwagger.RESULT_NAME_AFFILIATION_COUNTS
    tags = [StatsViewSwagger.TAG_DATAVERSES]

    def get_stats_result(self, request):
        """Return the StatsResult object for this statistic"""
        stats_datasets = StatsMakerDataverses(**request.GET.dict())

        pub_state = self.get_pub_state(request)

        if pub_state == self.PUB_STATE_ALL:
            stats_result = stats_datasets.get_dataverse_affiliation_counts()
        elif pub_state == self.PUB_STATE_UNPUBLISHED:
            stats_result = stats_datasets.get_dataverse_affiliation_counts_unpublished()
        else:
            stats_result = stats_datasets.get_dataverse_affiliation_counts_published()

        return stats_result


class DataverseTypeCounts(StatsViewSwagger):

    # Define the swagger attributes
    # Note: api_path must match the path in urls.py
    #
    api_path = '/dataverses/count/by-type'
    summary = ('Number of Dataverses by Type')
    description = ('Number of Dataverses by Type.')
    description_200 = 'Number of published Dataverses by Type.'
    param_names = StatsViewSwagger.PARAM_DV_API_KEY + StatsViewSwagger.PUBLISH_PARAMS +\
                    StatsViewSwagger.PRETTY_JSON_PARAM +\
                    StatsViewSwagger.DV_TYPE_UNCATEGORIZED_PARAM
    result_name = StatsViewSwagger.RESULT_NAME_DATAVERSE_TYPE_COUNTS
    tags = [StatsViewSwagger.TAG_DATAVERSES]

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

        pub_state = self.get_pub_state(request)

        if pub_state == self.PUB_STATE_ALL:
            stats_result = stats_datasets.get_dataverse_counts_by_type(exclude_uncategorized)
        elif pub_state == self.PUB_STATE_UNPUBLISHED:
            stats_result = stats_datasets.get_dataverse_counts_by_type_unpublished(exclude_uncategorized)
        else:
            stats_result = stats_datasets.get_dataverse_counts_by_type_published(exclude_uncategorized)

        return stats_result
